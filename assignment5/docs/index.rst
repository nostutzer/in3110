.. EnergyWebApp documentation master file, created by
   sphinx-quickstart on Fri Nov 18 20:13:33 2022.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Strømpris' documentation!
================================================
Do you want to know how the energy prices have developed 
in your region in Norway? Then this is the right tool for you!

Using the Strømpris web app you can download the electricity 
prices of five regions within Norway to make nice and informative
plots of the energy prices in NOK per kWh as a function of time.

To run web app simply type 

:code:`python -m app app.py`

in your terminal. Then simply copy and paste the URL that 
:code:`uvicorn` will provide in the terminal into your favorite
internet browser to get to the web app.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   app.rst
   strompris.rst


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
