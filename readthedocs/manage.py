#!/usr/bin/env python

import settings.postgres
from django.core.management import execute_manager
execute_manager(settings.postgres)
