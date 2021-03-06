
Slider
===============


.. topic:: General description

    The slider is used to change a value in a given interval.


.. figure:: _static/Slider.png
    :alt: Picture of the plugin slider

Configuration
----------------------
The plugin uses this specific configuration.

.. list-table:: Plugin configuration
    :widths: 15 10 30
    :header-rows: 1

    * - Name
      - Type
      - Description
    * - lower_bound
      - Float
      - Defines the lower interval bound.
    * - upper_bound
      - Float
      - Defines the upper interval bound.
    * - step_count
      - String
      - Defines the amount of steps between the upper and lower bound.
    * - value_init
      - Float
      - Used to set an initial value.
    * - vertical
      - Bool
      - Enables a vertical slider.

Parameter
----------------------
A plugin instance can be manipulated by the following parameter.

.. list-table:: Provided parameter
    :widths: 15 10 30
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
    :widths: 15 10 30
    :header-rows: 1

    * - Name
      - Type
      - Description
    * - Change
      - Float
      - Sent when slider was moved.
