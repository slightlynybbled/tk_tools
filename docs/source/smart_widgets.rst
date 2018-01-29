Smart Widgets
=============

Smart widgets consist of existing widgets with improved API.  In most cases, these widgets will simply incorporate the appropriate type of ``xVar`` for the widget type.  For instance, imaging providing for an ``OptionMenu`` without having to use a ``StringVar``.

``SmartOptionMenu``
-------------------

Example::

        # create the dropdown and grid
        som = SmartOptionMenu(root, ['one', 'two', 'three'])
        som.grid()

        # define a callback function that retrieves
        # the currently selected option
        def callback():
            print(som.get())

        # add the callback function to the dropdown
        som.add_callback(callback)

.. autoclass:: tk_tools.SmartOptionMenu
    :members:

``SmartSpinBox``
-----------------

.. autoclass:: tk_tools.SmartSpinBox
    :members:

``SmartCheckbutton``
--------------------

.. autoclass:: tk_tools.SmartCheckbutton
    :members:

``ByteLabel``
-------------

.. autoclass:: tk_tools.ByteLabel
    :members:
