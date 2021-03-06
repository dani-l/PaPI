
ProgressBar
===============


.. topic:: General description

    This plugin is used to show a progress

.. figure:: _static/ProgressBar.png
    :alt: Picture of the plugin ProgressBar

Configuration
----------------------
The plugin uses this specific configuration.

.. list-table:: Plugin configuration
    :widths: 15 10 10 50
    :header-rows: 1

    * - Name
      - Type
      - Example
      - Description
    * - progress_value
      - String
      - percent
      - Name of the signal whose first value is used to set the current value for the progress bar.
    * - show_percent
      - Bool
      - (1|0)
      - Show progress in percent over the progress bar.
    * - show_current_max
      - Bool
      - (1|0)
      - A label over the bar shows the current and max value.
    * - min_rage
      - Float
      - 0
      - Set minimum range for the progress bar..
    * - max_range
      - Float
      - 100
      - Set maximum range for the progress bar.
    * - trigger_value
      - String
      - trigger
      - Name of the signal which triggers the progress bar to increment by one.
    * - reset_trigger_value
      - String
      - reset
      - Name of the signal which triggers the progress bar to reset.
    * - round_digit
      - Int
      - 3
      - Current value is rounded to ndigits after the decimal point.

Parameter
----------------------
A plugin instance can be manipulated by the following parameter.

.. list-table:: Provided parameter
    :widths: 15 10 10 50
    :header-rows: 1

    * - Name
      - Type
      - Example
      - Description
    * - ProgressValue
      - String
      - percent
      - Name of the signal whose first value is used to set the current value for the progress bar.
    * - ShowPercent
      - Bool
      - (1|0)
      - Show progress in percent over the progress bar.
    * - ShowCurrentMax
      - Bool
      - (1|0)
      - A label over the bar shows the current and max value.
    * - MinRange
      - Float
      - 0
      - Set minimum range for the progress bar..
    * - MaxRange
      - Float
      - 100
      - Set maximum range for the progress bar.
    * - TriggerValue
      - String
      - trigger
      - Name of the signal which triggers the progress bar to increment by one.
    * - ResetValue
      - String
      - reset
      - Name of the signal which triggers the progress bar to reset.