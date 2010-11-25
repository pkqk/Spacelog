from django.views.generic import TemplateView
from backend.api import LogLine, Act
import redis

class PageView(TemplateView):

    template_name = 'transcripts/page.html'

    def get_context_data(self, timestamp):
        redis_conn = redis.Redis()

        acts = list(Act.Query(redis_conn, 'a13').items())
        if timestamp is None:
            timestamp = acts[0].start

        closest_log_line = LogLine.Query(redis_conn, 'a13').first_after(int(timestamp))
        page_number = closest_log_line.page
        log_lines = list(LogLine.Query(redis_conn, 'a13').transcript('a13/TEC').page(page_number))

        # Find the previous log line from this, and then the beginning of its page
        try:
            previous_timestamp = LogLine.Query(redis_conn, 'a13').transcript('a13/TEC').page(page_number - 1).first().timestamp
        except ValueError:
            previous_timestamp = None

        return {
            'page_number': page_number,
            'log_lines': log_lines,
            'next_timestamp': log_lines[-1].timestamp + 1,
            'previous_timestamp': previous_timestamp,
            'acts': acts,
            'current_act': log_lines[0].act(),
        }


class PhasesView(TemplateView):
    
    template_name = 'transcripts/phases.html'
    
    def get_context_data(self):
        redis_conn = redis.Redis()
        return {
            'acts': list(Act.Query(redis_conn, 'a13').items()),
        }


class RangeView(PageView):
    pass
