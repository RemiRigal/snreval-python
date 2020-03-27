#!/usr/bin/env python
# coding: utf-8

import os
import shlex
import signal
import pandas as pd
from subprocess import Popen, PIPE, TimeoutExpired


class SNREval(object):

    _DATAFRAME_COLUMNS = ["file", "STNR", "SNR"]

    def __init__(self, root):
        """
        :type root: str
        :param root: The location of the directory containing the script 'run_snreval_prj.sh'
        """
        self.root = root
        self.shell_script = os.path.join(root, "run_snreval_prj.sh")
        if not os.path.exists(self.shell_script):
            raise IOError("File 'run_snreval_prj.sh' not found at location {}".format(root))
        self.disp = 0
        self.guessvad = 0

    def eval(self, wave_file, timeout=None):
        """
        Note: it takes around 4 sec to load the script and ~0.1 sec to process a single file
        :type wave_file: str
        :param wave_file: Path to a .wav file or a .txt file listing .wav files
        :type timeout: float
        :param timeout: Timeout for the snreval process
        :rtype: pd.DataFrame
        :return: A DataFrame object containing estimated STNR and WADA SNR
        """
        if not os.path.exists(wave_file):
            raise IOError("File not found: {}".format(wave_file))
        command = self._get_command(wave_file)
        process = Popen(command, stdout=PIPE, stderr=PIPE, preexec_fn=os.setsid)
        try:
            result, errors = process.communicate(timeout=timeout)
        except TimeoutExpired:
            os.killpg(os.getpgid(process.pid), signal.SIGKILL)
            process.kill()
            result, errors = process.communicate()
        return self._parse_result(result.decode())

    def _get_command(self, file_path):
        """
        :type file_path: str
        :param file_path: Input file path (either .wav or .txt)
        :rtype: list of str
        :return: The shell command as a splitted shlex list
        """
        listin = 0 if file_path.endswith(".wav") else 1
        command = "sh {} {} -listout 1 -disp {} -listin {} -guessvad {}".format(
            self.shell_script, file_path, self.disp, listin, self.guessvad)
        return shlex.split(command)

    def _parse_result(self, result):
        """
        :type result: str
        :param result: The output produced by the SNR eval script
        :rtype: pd.DataFrame
        :return: A DataFrame object containing results
        """
        result = [l for l in result.split("\n") if l and not l.startswith("#") and not l.startswith("sndcat")]
        data = list()
        for line in result:
            splitted = line.split("\t")
            try:
                datum = [splitted[0], float(splitted[4]), float(splitted[5])]
                data.append(datum)
            except IndexError: pass
        return pd.DataFrame(data, columns=self._DATAFRAME_COLUMNS)
