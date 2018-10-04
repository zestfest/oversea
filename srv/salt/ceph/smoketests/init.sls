{# Include the two most likely migrations, others can be run ad hoc #}
include:
  - .keyrings
  - .macros.os_switch
  - .quiescent
  - .restart
  - .replace
  - .remove
  - .migrate.filestore.bluestore
  - .migrate.filestore2.bluestore2
