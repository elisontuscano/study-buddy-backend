from invoke import Collection

import tasks.requirements
import tasks.about
import tasks.stack
import tasks.build

ns = Collection()

# Add all our separate task files as sub-collections
ns.add_collection(tasks.requirements, name="req")
ns.add_collection(tasks.about, name="about")
ns.add_collection(tasks.stack, name="stack")
ns.add_collection(tasks.build, name="build")

ns.add_task(tasks.about.info, name="info")
