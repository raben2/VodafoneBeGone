import time
import random
import speedtest 
from fast_com import fast_com
from prometheus_client import Metric


class Collector(object):
    def __init__(self, endpoint, service, exclude=list):
        self._endpoint = endpoint
        self._service = service
        self._labels = {}
        self._set_labels()
        self._exclude = exclude

    def _set_labels(self):
        self._labels.update({'service': self._service})

    def filter_exclude(self, metrics):
        return {k: v for k, v in metrics.items() if k not in self._exclude}
    def do_nothing(*args, **kwargs):
        pass
    def run_speedtest(self):
        st = speedtest.Speedtest(timeout=18,
            secure=True)
        server = st.get_best_server()
        config = st.get_config()
        download = st.download(callback=self.do_nothing)
        upload = st.upload(callback=self.do_nothing)
        ping = st.results.ping
        return download, upload, ping

    def _get_metrics(self):
        download, upload, ping = self.run_speedtest()

        metrics = {
            'speedtest_download': format((download / 1000.0 / 1000.0), '.2f'),
            'speedtest_upload':  format((upload / 1000.0 / 1000.0), '.2f'),
            'speedtest_ping' : ping,
            'fast_com_ipv4': fast_com(verbose=False, maxtime=18, forceipv4=True),
            'fast_com_ipv6': fast_com(verbose=False, maxtime=18, forceipv6=True),
            'fast_com_default': fast_com(verbose=False, maxtime=18),
          }

        if self._exclude:
            metrics = self.filter_exclude(metrics)

        time.sleep(random.uniform(0.1, 0.4))
        return metrics

    def collect(self):
        metrics = self._get_metrics()

        if metrics:
            for k, v in metrics.items():
                metric = Metric(k, k, 'counter')
                labels = {}
                labels.update(self._labels)
                metric.add_sample(k, value=v, labels=labels)

                if metric.samples:
                    yield metric
                else:
                    pass