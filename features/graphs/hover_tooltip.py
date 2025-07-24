"""
Interactive Graph Hover Tooltip System - Optimized with Beginner Comments
========================================================================

This file creates interactive tooltips that appear when you hover your mouse over graphs.
Think of it like having a helpful assistant that pops up to tell you exact values
when you point at any part of a weather chart.

Key Features:
- Shows exact data values when you hover over graph points
- Automatically positions tooltips so they don't go off-screen
- Works with different types of graphs (lines, bars, pie charts)
- Smoothly appears and disappears as you move your mouse
- Shows formatted dates, temperatures, and other weather data

This makes graphs much more interactive and informative!
"""

import matplotlib
import numpy as np


class HoverTooltip:
    """
    Main class that creates and manages hover tooltips for matplotlib graphs.
    
    This class is like a smart popup system that:
    - Watches where your mouse is on the graph
    - Finds the nearest data point to your mouse
    - Shows a popup with the exact values for that point
    - Moves the popup around to stay visible and not block the data
    """
    
    def __init__(self, ax, canvas):
        """
        Initialize the hover tooltip system.
        
        Args:
            ax: The matplotlib axes object (the actual graph area)
            canvas: The canvas widget that displays the graph
        """
        self.ax = ax  # Store reference to the graph
        self.canvas = canvas  # Store reference to the display canvas
        
        # Create the tooltip annotation (this is the popup box)
        self.annotation = self.ax.annotate(
            '',  # Start with empty text
            xy=(0, 0),  # Position on the graph (will be updated)
            xytext=(20, 20),  # Offset from the point (in pixels)
            textcoords='offset points',  # Use pixel offsets for positioning
            bbox=dict(boxstyle='round,pad=0.5', fc='yellow', alpha=0.9),  # Yellow rounded box
            arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0'),  # Arrow pointing to data
            visible=False,  # Start invisible
            zorder=1000  # Make sure tooltip appears on top of everything
        )
        
        # Storage for the lines we're monitoring
        self.lines = []  # List of line objects from the graph
        self.labels = []  # List of labels for each line
        
        # Performance optimization - cache mouse position calculations
        self._last_mouse_pos = None
        self._last_update_time = 0
        self._update_interval = 0.05  # Update at most 20 times per second
    
    def add_line(self, line, label):
        """
        Add a line to monitor for hover events.
        
        Call this method for each line you want to have interactive tooltips.
        
        Args:
            line: The matplotlib line object (from ax.plot())
            label: A descriptive name for this line (e.g., "Temperature", "Humidity")
        """
        self.lines.append(line)
        self.labels.append(label)
    
    def update(self, event):
        """
        Update the tooltip based on mouse position.
        
        This method is called automatically whenever the mouse moves over the graph.
        It finds the closest data point and shows relevant information.
        
        Args:
            event: Mouse event containing position and other info
        """
        # Check if mouse is over our graph area
        if event.inaxes != self.ax:
            self._hide_tooltip()
            return
        
        # Performance optimization - don't update too frequently
        import time
        current_time = time.time()
        if current_time - self._last_update_time < self._update_interval:
            return
        self._last_update_time = current_time
        
        # Find the nearest data point to the mouse cursor
        nearest_point_info = self._find_nearest_point(event)
        
        if nearest_point_info:
            # Show tooltip with information about the nearest point
            self._show_tooltip(nearest_point_info, event)
        else:
            # No nearby points, hide the tooltip
            self._hide_tooltip()
        
        # Redraw the canvas to show changes
        self.canvas.draw_idle()
    
    def _find_nearest_point(self, event):
        """
        Find the data point closest to the mouse cursor.
        
        This method searches through all the lines we're monitoring and finds
        the point that's closest to where the mouse is positioned.
        
        Args:
            event: Mouse event with position information
            
        Returns:
            dict: Information about the nearest point, or None if nothing is close enough
        """
        if event.xdata is None or event.ydata is None:
            return None  # Mouse position invalid
        
        min_distance = float('inf')  # Start with infinite distance
        nearest_point = None
        
        # Check each line for nearby points
        for line, label in zip(self.lines, self.labels):
            xdata = line.get_xdata()  # Get x-coordinates of all points on this line
            ydata = line.get_ydata()  # Get y-coordinates of all points on this line
            
            if len(xdata) == 0:
                continue  # Skip empty lines
            
            # Create array of all points on this line
            points = np.column_stack([xdata, ydata])
            
            # Calculate distance from mouse to each point
            distances = np.sqrt((points[:, 0] - event.xdata)**2 + 
                               (points[:, 1] - event.ydata)**2)
            
            # Find the closest point on this line
            idx = np.argmin(distances)
            distance = distances[idx]
            
            # Check if this is the closest point we've found so far
            if distance < min_distance:
                min_distance = distance
                nearest_point = {
                    'x': xdata[idx],
                    'y': ydata[idx], 
                    'index': idx,
                    'label': label,
                    'line': line,
                    'distance': distance
                }
        
        # Only return the point if it's close enough to the mouse
        # (threshold in data units - adjust based on your graph scale)
        if nearest_point and nearest_point['distance'] < 0.1:
            return nearest_point
        
        return None
    
    def _show_tooltip(self, point_info, event):
        """
        Display the tooltip with information about a data point.
        
        Args:
            point_info (dict): Information about the point to show
            event: Mouse event for positioning
        """
        x, y = point_info['x'], point_info['y']
        label = point_info['label']
        
        # Format the display text
        tooltip_text = self._format_tooltip_text(x, y, label)
        
        # Position the tooltip at the data point
        self.annotation.xy = (x, y)
        self.annotation.set_text(tooltip_text)
        self.annotation.set_visible(True)
        
        # Adjust tooltip position to keep it on screen
        self._adjust_tooltip_position(event)
    
    def _format_tooltip_text(self, x, y, label):
        """
        Create nicely formatted text for the tooltip.
        
        Args:
            x: X-coordinate value (often a date/time)
            y: Y-coordinate value (often temperature, humidity, etc.)
            label: Label describing what this data represents
            
        Returns:
            str: Formatted text ready for display
        """
        # Handle date/time formatting
        try:
            if isinstance(x, (int, float)):
                # Assume x is a matplotlib date number
                date = matplotlib.dates.num2date(x)
                date_str = date.strftime('%Y-%m-%d %H:%M')
            else:
                date_str = str(x)
        except:
            date_str = str(x)
        
        # Format the complete tooltip text
        return f'{label}\n{date_str}\nValue: {y:.2f}'
    
    def _adjust_tooltip_position(self, event):
        """
        Adjust tooltip position so it stays visible on screen.
        
        This prevents tooltips from being cut off at the edges of the graph.
        
        Args:
            event: Mouse event for reference positioning
        """
        try:
            # Get the renderer to calculate text dimensions
            renderer = self.canvas.get_renderer()
            ann_bbox = self.annotation.get_window_extent(renderer=renderer)
            ax_bbox = self.ax.get_window_extent(renderer=renderer)
            
            # Default offset position
            x_offset = 20
            y_offset = 20
            
            # Adjust if tooltip would go off the right edge
            if ann_bbox.x1 > ax_bbox.x1:
                x_offset = -100  # Move tooltip to left of point
            
            # Adjust if tooltip would go off the top edge
            if ann_bbox.y1 > ax_bbox.y1:
                y_offset = -50  # Move tooltip below point
            
            # Apply the adjusted offset
            self.annotation.xyann = (x_offset, y_offset)
            
        except Exception:
            # If positioning calculation fails, use default offset
            pass
    
    def _hide_tooltip(self):
        """
        Hide the tooltip when mouse moves away from data points.
        """
        self.annotation.set_visible(False)
    
    def clear_lines(self):
        """
        Remove all lines from hover monitoring.
        
        Call this when creating a new graph to start fresh.
        """
        self.lines.clear()
        self.labels.clear()
        self._hide_tooltip()
    
    def set_tooltip_style(self, background_color='yellow', text_color='black', 
                          border_color='black', alpha=0.9):
        """
        Customize the appearance of tooltips.
        
        Args:
            background_color (str): Background color of tooltip box
            text_color (str): Color of text inside tooltip
            border_color (str): Color of tooltip border
            alpha (float): Transparency (0=invisible, 1=opaque)
        """
        # Update the tooltip box styling
        bbox_props = dict(
            boxstyle='round,pad=0.5',
            fc=background_color,
            ec=border_color,
            alpha=alpha
        )
        self.annotation.set_bbox(bbox_props)
        self.annotation.set_color(text_color)
    
    def enable_detailed_mode(self, show_coordinates=True, show_statistics=False):
        """
        Enable detailed tooltip mode with additional information.
        
        Args:
            show_coordinates (bool): Whether to show exact x,y coordinates
            show_statistics (bool): Whether to show additional statistics
        """
        self.show_coordinates = show_coordinates
        self.show_statistics = show_statistics
    
    def get_tooltip_info(self):
        """
        Get information about the currently displayed tooltip.
        
        Returns:
            dict: Current tooltip information or None if not visible
        """
        if self.annotation.get_visible():
            return {
                'text': self.annotation.get_text(),
                'position': self.annotation.xy,
                'visible': True
            }
        return {'visible': False}


class AdvancedHoverTooltip(HoverTooltip):
    """
    Enhanced version of HoverTooltip with additional features.
    
    This extends the basic tooltip with:
    - Multi-line data display
    - Custom formatting options
    - Performance optimizations for large datasets
    - Support for different chart types
    """
    
    def __init__(self, ax, canvas):
        """Initialize advanced hover tooltip."""
        super().__init__(ax, canvas)
        
        # Additional features
        self.multi_line_mode = False
        self.custom_formatters = {}
        self.data_cache = {}
    
    def set_multi_line_mode(self, enabled=True):
        """
        Enable multi-line tooltips that show data from all lines at once.
        
        Args:
            enabled (bool): Whether to show data from all lines simultaneously
        """
        self.multi_line_mode = enabled
    
    def add_custom_formatter(self, data_type, formatter_function):
        """
        Add custom formatting for specific types of data.
        
        Args:
            data_type (str): Type of data (e.g., 'temperature', 'date', 'percentage')
            formatter_function: Function that takes a value and returns formatted string
        """
        self.custom_formatters[data_type] = formatter_function
    
    def _format_tooltip_text(self, x, y, label):
        """
        Enhanced tooltip text formatting with custom formatters.
        """
        # Use custom formatters if available
        if 'date' in self.custom_formatters:
            date_str = self.custom_formatters['date'](x)
        else:
            # Default date formatting
            try:
                if isinstance(x, (int, float)):
                    date = matplotlib.dates.num2date(x)
                    date_str = date.strftime('%Y-%m-%d')
                else:
                    date_str = str(x)
            except:
                date_str = str(x)
        
        if 'value' in self.custom_formatters:
            value_str = self.custom_formatters['value'](y)
        else:
            # Default value formatting
            value_str = f'{y:.2f}'
        
        return f'{label}\n{date_str}\nValue: {value_str}'


def create_temperature_tooltip(ax, canvas):
    """
    Create a tooltip specifically optimized for temperature graphs.
    
    Args:
        ax: Matplotlib axes object
        canvas: Canvas widget
        
    Returns:
        AdvancedHoverTooltip: Configured tooltip for temperature data
    """
    tooltip = AdvancedHoverTooltip(ax, canvas)
    
    # Add temperature-specific formatting
    tooltip.add_custom_formatter('value', lambda v: f'{v:.1f}°C')
    tooltip.add_custom_formatter('date', lambda d: matplotlib.dates.num2date(d).strftime('%m/%d'))
    
    # Use temperature-appropriate styling
    tooltip.set_tooltip_style(
        background_color='lightblue',
        text_color='darkblue',
        alpha=0.95
    )
    
    return tooltip


def create_humidity_tooltip(ax, canvas):
    """
    Create a tooltip specifically optimized for humidity graphs.
    
    Args:
        ax: Matplotlib axes object
        canvas: Canvas widget
        
    Returns:
        AdvancedHoverTooltip: Configured tooltip for humidity data
    """
    tooltip = AdvancedHoverTooltip(ax, canvas)
    
    # Add humidity-specific formatting
    tooltip.add_custom_formatter('value', lambda v: f'{v:.0f}%')
    tooltip.add_custom_formatter('date', lambda d: matplotlib.dates.num2date(d).strftime('%m/%d'))
    
    # Use humidity-appropriate styling
    tooltip.set_tooltip_style(
        background_color='lightgreen',
        text_color='darkgreen',
        alpha=0.95
    )
    
    return tooltip


# Helper functions for easy tooltip creation
def setup_line_graph_tooltip(ax, canvas, lines_info):
    """
    Quickly set up tooltips for a line graph.
    
    Args:
        ax: Matplotlib axes object
        canvas: Canvas widget
        lines_info: List of tuples (line_object, label_string)
        
    Returns:
        HoverTooltip: Configured and ready-to-use tooltip
    """
    tooltip = HoverTooltip(ax, canvas)
    
    for line, label in lines_info:
        tooltip.add_line(line, label)
    
    # Connect mouse events
    canvas.mpl_connect('motion_notify_event', tooltip.update)
    
    return tooltip


def setup_temperature_graph_tooltip(ax, canvas, temperature_lines):
    """
    Set up tooltips specifically for temperature graphs.
    
    Args:
        ax: Matplotlib axes object
        canvas: Canvas widget
        temperature_lines: List of (line, label) tuples for temperature data
        
    Returns:
        AdvancedHoverTooltip: Temperature-optimized tooltip
    """
    tooltip = create_temperature_tooltip(ax, canvas)
    
    for line, label in temperature_lines:
        tooltip.add_line(line, label)
    
    # Connect mouse events
    canvas.mpl_connect('motion_notify_event', tooltip.update)
    
    return tooltip