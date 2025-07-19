class ScrollHandler:
    """
    Scroll Handler
    
    Manages scrolling functionality including scrollbar interaction,
    mouse wheel events, and widget position updates during scrolling.
    """
    
    def __init__(self, app, gui_controller):
        self.app = app
        self.gui = gui_controller
        
        # Scrolling state
        self.scroll_offset = 0
        self.max_scroll = 500
        
        # Position constants for scrolling calculations
        self.base_positions = {
            'metric_headers': 30,
            'metric_emojis': 55,
            'metric_values': 80,
            'theme_btn': 120,
            'city_entry': 160,
            'icon_label': 220,
            'temp_label': 290,
            'desc_label': 350,
            'prediction_title': 410,
            'prediction_headers': 440,
            'prediction_emojis': 465,
            'prediction_values': 490,
            'history_title': 550,
            'history_start': 590
        }

    def bind_scroll_events(self):
        """Bind scroll-related events to the application"""
        # Mouse wheel events
        self.app.bind_all("<MouseWheel>", self.on_mousewheel)
        self.app.bind_all("<Button-4>", self.on_mousewheel)  # Linux scroll up
        self.app.bind_all("<Button-5>", self.on_mousewheel)  # Linux scroll down

    def on_scroll(self, *args):
        """Handle scrollbar movement"""
        if len(args) >= 2:
            scroll_type = args[0]
            if scroll_type == "moveto":
                # Handle scrollbar drag
                fraction = float(args[1])
                self.scroll_offset = int(fraction * self.max_scroll)
                self.update_widget_positions()
            elif scroll_type in ["scroll", "units"]:
                # Handle scrollbar click
                direction = int(args[1])
                scroll_amount = 20
                self.scroll_offset += direction * scroll_amount
                self.scroll_offset = max(0, min(self.scroll_offset, self.max_scroll))
                self.update_widget_positions()

    def on_mousewheel(self, event):
        """Handle mouse wheel scrolling"""
        # Determine scroll direction and amount
        if hasattr(event, 'delta') and event.delta:
            # Windows mouse wheel
            scroll_amount = -int(event.delta / 120) * 20
        elif hasattr(event, 'num'):
            if event.num == 4:
                # Linux scroll up
                scroll_amount = -20
            elif event.num == 5:
                # Linux scroll down
                scroll_amount = 20
            else:
                return
        else:
            return
        
        # Update scroll offset with bounds checking
        old_offset = self.scroll_offset
        self.scroll_offset += scroll_amount
        self.scroll_offset = max(0, min(self.scroll_offset, self.max_scroll))
        
        # Only update if scroll actually changed
        if self.scroll_offset != old_offset:
            self.update_widget_positions()
            self.update_scrollbar_position()

    def update_widget_positions(self):
        """Update all widget positions based on current scroll offset"""
        try:
            window_width = self.app.winfo_width()
            
            # Calculate responsive layout values
            available_width = window_width - 40
            metrics_col_width = available_width / 6
            prediction_col_width = available_width / 3
            start_x = 20
            
            # Update all widgets in the main widgets list
            self._update_main_widgets()
            
            # Update specifically positioned named widgets
            self._update_named_widgets(window_width, metrics_col_width, prediction_col_width, start_x)
            
            # Update history labels
            self._update_history_positions()
            
        except Exception as e:
            print(f"❌ Position update error: {e}")

    def _update_main_widgets(self):
        """Update positions of widgets in the main widgets list"""
        for i, widget in enumerate(self.gui.widgets):
            try:
                place_info = widget.place_info()
                if not place_info:
                    continue
                
                current_x = float(place_info.get('x', 0))
                base_y = self._determine_widget_base_y(i)
                
                # Apply scroll offset
                new_y = base_y - self.scroll_offset
                widget.place(x=current_x, y=new_y, anchor="center")
                
            except Exception:
                continue

    def _determine_widget_base_y(self, widget_index):
        """Determine the base Y position for a widget based on its index"""
        # Map widget indices to their base Y positions
        if widget_index < 6:  # Weather metric headers
            return self.base_positions['metric_headers']
        elif widget_index < 12:  # Weather metric emojis
            return self.base_positions['metric_emojis']
        elif widget_index < 18:  # Weather metric values
            return self.base_positions['metric_values']
        elif widget_index == 18:  # Theme button
            return self.base_positions['theme_btn']
        elif widget_index == 19:  # City entry
            return self.base_positions['city_entry']
        elif widget_index == 20:  # Icon label
            return self.base_positions['icon_label']
        elif widget_index == 21:  # Temperature label
            return self.base_positions['temp_label']
        elif widget_index == 22:  # Description label
            return self.base_positions['desc_label']
        elif widget_index == 23:  # Prediction title
            return self.base_positions['prediction_title']
        elif widget_index < 27:  # Prediction headers
            return self.base_positions['prediction_headers']
        elif widget_index < 30:  # Prediction emojis
            return self.base_positions['prediction_emojis']
        elif widget_index < 33:  # Prediction values
            return self.base_positions['prediction_values']
        elif widget_index == 33:  # History title
            return self.base_positions['history_title']
        else:
            # Default fallback
            return 100

    def _update_named_widgets(self, window_width, metrics_col_width, prediction_col_width, start_x):
        """Update positions of specifically named widgets"""
        # Weather metrics widgets
        metric_widgets = [
            (self.gui.humidity_value, start_x + (0 * metrics_col_width) + (metrics_col_width / 2)),
            (self.gui.wind_value, start_x + (1 * metrics_col_width) + (metrics_col_width / 2)),
            (self.gui.pressure_value, start_x + (2 * metrics_col_width) + (metrics_col_width / 2)),
            (self.gui.visibility_value, start_x + (3 * metrics_col_width) + (metrics_col_width / 2)),
            (self.gui.uv_value, start_x + (4 * metrics_col_width) + (metrics_col_width / 2)),
            (self.gui.precipitation_value, start_x + (5 * metrics_col_width) + (metrics_col_width / 2)),
        ]
        
        # Main display widgets
        main_widgets = [
            (self.gui.theme_btn, window_width / 2, self.base_positions['theme_btn']),
            (self.gui.city_entry, window_width / 2, self.base_positions['city_entry']),
            (self.gui.icon_label, window_width / 2, self.base_positions['icon_label']),
            (self.gui.temp_label, window_width / 2, self.base_positions['temp_label']),
            (self.gui.desc_label, window_width / 2, self.base_positions['desc_label']),
        ]
        
        # Prediction widgets
        prediction_widgets = [
            (self.gui.temp_prediction, start_x + (0 * prediction_col_width) + (prediction_col_width / 2)),
            (self.gui.accuracy_prediction, start_x + (1 * prediction_col_width) + (prediction_col_width / 2)),
            (self.gui.confidence_prediction, start_x + (2 * prediction_col_width) + (prediction_col_width / 2)),
        ]
        
        # Update metric widgets
        for widget, x_pos in metric_widgets:
            if widget:
                try:
                    new_y = self.base_positions['metric_values'] - self.scroll_offset
                    widget.place(x=x_pos, y=new_y, anchor="center")
                except Exception:
                    pass
        
        # Update main widgets
        for widget, x_pos, base_y in main_widgets:
            if widget:
                try:
                    new_y = base_y - self.scroll_offset
                    widget.place(x=x_pos, y=new_y, anchor="center")
                except Exception:
                    pass
        
        # Update prediction widgets
        for widget, x_pos in prediction_widgets:
            if widget:
                try:
                    new_y = self.base_positions['prediction_values'] - self.scroll_offset
                    widget.place(x=x_pos, y=new_y, anchor="center")
                except Exception:
                    pass

    def _update_history_positions(self):
        """Update history label positions during scrolling"""
        try:
            window_width = self.app.winfo_width()
            start_y = self.base_positions['history_start']
            
            # Calculate responsive positioning for history
            history_labels = self.gui.history_labels
            history_count = min(7, len(history_labels) // 4) if history_labels else 0
            
            if history_count > 0:
                available_width = window_width - 40
                col_width = available_width / history_count
                start_x = 20
                
                for col in range(history_count):
                    col_start_idx = col * 4
                    if col_start_idx + 3 < len(history_labels):
                        x_pos = start_x + (col * col_width) + (col_width / 2)
                        
                        # Apply scroll offset to all history elements
                        if col_start_idx < len(history_labels):
                            history_labels[col_start_idx].place(
                                x=x_pos, y=start_y - self.scroll_offset, anchor="center"
                            )
                        if col_start_idx + 1 < len(history_labels):
                            history_labels[col_start_idx + 1].place(
                                x=x_pos, y=(start_y + 25) - self.scroll_offset, anchor="center"
                            )
                        if col_start_idx + 2 < len(history_labels):
                            history_labels[col_start_idx + 2].place(
                                x=x_pos, y=(start_y + 50) - self.scroll_offset, anchor="center"
                            )
                        if col_start_idx + 3 < len(history_labels):
                            history_labels[col_start_idx + 3].place(
                                x=x_pos, y=(start_y + 75) - self.scroll_offset, anchor="center"
                            )
        except Exception as e:
            print(f"❌ History position update error: {e}")

    def update_scrollbar_position(self):
        """Update scrollbar position to reflect current scroll offset"""
        try:
            if hasattr(self.gui, 'scrollbar') and self.gui.scrollbar:
                fraction = self.scroll_offset / self.max_scroll if self.max_scroll > 0 else 0
                self.gui.scrollbar.set(fraction, fraction + 0.1)
        except Exception:
            pass

    def get_scroll_offset(self):
        """Get current scroll offset"""
        return self.scroll_offset

    def set_scroll_offset(self, offset):
        """Set scroll offset with bounds checking"""
        self.scroll_offset = max(0, min(offset, self.max_scroll))

    def reset_scroll(self):
        """Reset scroll to top"""
        self.scroll_offset = 0
        self.update_widget_positions()
        self.update_scrollbar_position()