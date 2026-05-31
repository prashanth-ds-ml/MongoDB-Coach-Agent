import certcoach.core.planner as planner

status = planner.get_syllabus_status('default_user')
print(f"Skipped topics count: {len(status['skipped_unmapped_topics'])}")
for item in status['skipped_unmapped_topics']:
    print(f"  - Topic #{item['id']}: {item['topic']}")
print(f"Next Topic: {status['next_topic']['topic'] if status['next_topic'] else None}")
