import threading, logging, multiprocessing
from requests import Session

websites = {
    'example': ['https://example.com'],
    'exampleweb': ['https://exampleweb.com']
}

class MyThread(threading.Thread):
    def __init__(self, org_name : str = "", web_link : str = "", *args, **kwargs):
        logging.basicConfig(filename="websites.log",
            format='%(asctime)s %(message)s',
            filemode='a'
        )
        self.not_errors = [200,]
        self.timeout = (1, 20)
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.DEBUG)
        self.request = Session().request

        self.org_name = org_name
        self.web_link = web_link # str

        threading.Thread.__init__(self)

    def error_log(self, org_name, website, status_code):
        self.logger.error(
            f'(Error) => Org: {org_name}, Web: {website}, Status Code: {status_code}'
        )

    def info_log(self, org_name, website, status_code):
        self.logger.info(
            f'(Info) => Org: {org_name}, Web: {website}, Status Code: {status_code}'
        )

    def make_request(self, url):
        try:
            response = self.request(
                'GET',
                url,
                verify=True,
                timeout=self.timeout
            )
        except:
            self.info_log(
                self.org_name, url, 'RedCode'
            )
        else:
            if response.status_code not in self.not_errors:
                self.info_log(
                    self.org_name, url, response.status_code
                )
            else:
                self.info_log(
                    self.org_name, url, response.status_code
                )

    def run(self):
        print(f'monitoring -> {self.web_link}')
        self.make_request(
            self.web_link
        )

if __name__ == "__main__":
    threads = []

    for org, web in websites.items():
        for url in web:

            MyTh = MyThread(org, url)

            threads.append(
                MyTh
            )

            MyTh.start()

    for t in threads: t.join()
