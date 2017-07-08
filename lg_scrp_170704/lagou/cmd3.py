# -*- coding: utf-8 -*-
from scrapy.cmdline import execute

import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
# execute(["scrapy", "crawl", "get_all_search"])
# execute(["scrapy", "crawl", "get_comp"])
execute(["scrapy", "crawl", "get_job_list_new2"])

# execute(["scrapy", "crawl", "get_job_list"])
# execute(["scrapy", "crawl", "get_job_detail"])