import tornado.ioloop
import tornado.web
from services.qa_service import QAService, QAHealthCheck


def make_app():
    return tornado.web.Application([
        (r"/predict", QAService),
        (r"/health", QAHealthCheck)
    ])


if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()