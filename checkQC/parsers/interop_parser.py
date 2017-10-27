
from checkQC.parsers.parser import Parser

from interop import py_interop_run_metrics, py_interop_run, py_interop_summary


class InteropParser(Parser):

    def __init__(self, runfolder, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.runfolder = runfolder

    @staticmethod
    def get_non_index_reads(summary):
        # First pick-out the reads which are not index reads
        non_index_reads = []
        for read_nbr in range(summary.size()):
            if not summary.at(read_nbr).read().is_index():
                non_index_reads.append(read_nbr)
        return non_index_reads

    def run(self):

        run_metrics = py_interop_run_metrics.run_metrics()
        run_metrics.run_info()

        valid_to_load = py_interop_run.uchar_vector(py_interop_run.MetricCount, 0)
        py_interop_run_metrics.list_summary_metrics_to_load(valid_to_load)
        run_metrics.read(self.runfolder, valid_to_load)

        summary = py_interop_summary.run_summary()
        py_interop_summary.summarize_run_metrics(run_metrics, summary)

        lanes = summary.lane_count()
        reads = self.get_non_index_reads(summary)
        for lane in range(lanes):
            # The interop library uses zero based indexing, however most people uses read 1/2
            # to denote the different reads, this enumeration is used to transform from
            # zero based indexing to this form. /JD 2017-10-27
            for new_read_nbr, original_read_nbr in enumerate(reads):
                read = summary.at(original_read_nbr).at(lane)
                error_rate = read.error_rate().mean()
                percent_q30 = read.percent_gt_q30()
                self._send_to_subscribers(("error_rate",
                                           {"lane": lane+1, "read": new_read_nbr+1, "error_rate": error_rate}))
                self._send_to_subscribers(("percent_q30",
                                           {"lane": lane+1, "read": new_read_nbr+1, "percent_q30": percent_q30}))

    def __eq__(self, other):
        if isinstance(other, self.__class__) and self.runfolder == other.runfolder:
            return True
        else:
            return False

    def __hash__(self):
        return hash(self.__class__.__name__ + self.runfolder)
