from django.template.loader import render_to_string

from debug_toolbar.panels import DebugPanel

from operation_tracker import MongoOperationTracker


class MongoDebugPanel(DebugPanel):
    """Panel that shows information about MongoDB queries.
    """
    name = 'MongoDB'
    has_content = True

    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        self.op_tracker = MongoOperationTracker()
        self.op_tracker.install()

    def process_request(self, request):
        self.op_tracker.reset()
        self.op_tracker.start()

    def process_response(self, request, response):
        self.op_tracker.stop()

    def nav_title(self):
        return 'MongoDB'

    def nav_subtitle(self):
        num_queries = len(self.op_tracker.queries)
        total_time = sum(q['time'] for q in self.op_tracker.queries)
        return '{0} operations in {1:.2f}ms'.format(num_queries, total_time)

    def title(self):
        return 'MongoDB Queries'

    def url(self):
        return ''

    def content(self):
        context = self.context.copy()
        context['queries'] = self.op_tracker.queries
        return render_to_string('mongo-panel.html', context)

