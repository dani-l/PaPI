
Button
===============


.. topic:: General description

    This button is used to switch between two given values which are defined by two different states.
    It is also possible to set a name for each state.

.. figure:: _static/Button.png
    :alt: Picture of the plugin button

Configuration
----------------------
The plugin uses this specific configuration.

.. list-table:: Plugin configuration
    :widths: 10 10 30
    :header-rows: 1

    * - Name
      - Type
      - Description
    * - state1
      - Float
      - Number which is sent when this state is active
    * - state2
      - Float
      - Number which is sent when this state is active
    * - state1_text
      - String
      - Displayed text when this state is active
    * - state2_text
      - String
      - Displayed text when this state is active

Parameter
----------------------
A plugin instance can be manipulated by the following parameter.

.. list-table:: Provided parameter
    :widths: 10 10 30
    :header-rows: 1

    * - Name
      - Type
      - Description
    * - None
      - None
      - None

Events
----------------------
A plugin instance provides this events which can be used to manipulated parameters of other plugins.

.. list-table:: Provided events
    :widths: 10 10 30
    :header-rows: 1

    * - Name
      - Type
      - Description
    * - Click
      - Float
      - Sent on every click on the button.
