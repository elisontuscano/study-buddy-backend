from invoke import Collection

import tasks.requirements
import tasks.about

ns = Collection()

# Add all our separate task files as sub-collections
ns.add_collection(tasks.requirements, name="req")
ns.add_collection(tasks.about, name="about")

ns.add_task(tasks.about.info, name="info")
