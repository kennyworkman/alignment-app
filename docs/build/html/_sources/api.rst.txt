.. _api:

API
===

This part of the documentation covers the application interface.
For functional dependencies on external libraries, links to relevant
documentation is provided.

The App Factory
---------------

.. autofunction:: alignment.create_app

The Frontend
------------

View Function
*************
.. autofunction:: alignment.frontend.index

The Forms
*********

.. autoclass:: alignment.forms.AlignForm
.. autoclass:: alignment.forms.AnotherForm
.. autoclass:: alignment.forms.SettingsForm

Alignment Functionality
-----------------------

.. autofunction:: alignment.clustalo_align.run_clustalo
.. autofunction:: alignment.clustalo_align.capture_alignment

Database API
------------

.. autofunction:: alignment.db.get_db
.. autofunction:: alignment.db.close_db
.. autofunction:: alignment.db.insert_genes
.. autofunction:: alignment.db.query_genes
.. autofunction:: alignment.db.wipe_genes
.. autofunction:: alignment.db.wipe_all_genes
.. autofunction:: alignment.db.get_gene_dict
.. autofunction:: alignment.db.init_db
.. autofunction:: alignment.db.init_db_command
.. autofunction:: alignment.db.init_app
