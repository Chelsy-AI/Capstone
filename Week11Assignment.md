## 🔖 Section 0: Fellow Details

| Field                   | Your Entry                          |
| ----------------------- | ----------------------------------- |
| Name                    | Drashti Patel                       |
| GitHub Username         | Chelsy                              |
| Preferred Feature Track | Data / Visual / Interactive / Smart |
| Team Interest           | Yes: Project Contributor            |

---------------------------------------------------------------------------------------------------------------------------

## ✍️ Section 1: Week 11 Reflection

### Key Takeaways

- The capstone project is structured to help us build something real, personal, and portfolio-ready.

- Weekly progress ensures we balance learning with delivery and avoid falling behind.

- Feature selection is key — I need to balance challenge with feasibility.

- Modular architecture (folders per feature) keeps code manageable as it grows.

- Documentation and GitHub hygiene matter from Day 1.

### Concept Connections

- Strongest skills: API integration, Python functions, error handling, and file I/O.

- Areas needing practice: GUI structuring in customtkinter, theme management, layout tuning.

- Confident with organizing modular files, working with real data, and working with version control.

### Early Challenges

- Setting up modular GUI across multiple files without breaking widget references.

- Initial confusion over how to integrate weather history display in grid layout.

- Some missing icons in the customtkinter interface due to file path issues.

### Support Strategies

- Using office hours to debug GUI display problems and theme toggling issues.

- Asking for best practices when managing per-feature folders and separation of GUI logic.

- Referring to prior class examples for data formatting and design inspiration.

---------------------------------------------------------------------------------------------------------------------------

## 🧠 Section 2: Feature Selection Rationale

| # | Feature Name            | Difficulty (1–3) | Why You Chose It / Learning Goal                                       |
| - | ----------------------- | ---------------- | ---------------------------------------------------------------------- |
| 1 | Weather History Tracker | 1                | Practice API + file storage, display real 7-day history in the UI      |
| 2 | Weather Alerts          | 2                | Add logic & interactivity, notify on extreme conditions                |
| 3 | Tomorrow’s Guess        | 3                | Learn basic prediction logic, show estimated forecast from past trends |
| 4 | Temperature Graph       | 2                | Visualize data with matplotlib, improve data readability               |
| 5 | Weather Icons           | 2                | Replace text with emojis/icons for a polished UI                       |
| 6 | Theme Switcher          | 2                | Improve usability via light/dark modes (already integrated)            |
| — | **Creative Visuals**    | —                | 🌟 Enhancement: Add animations, styled graphics, or emoji flair        |

---------------------------------------------------------------------------------------------------------------------------

## 🗂️ Section 3: High-Level Architecture Sketch

### 🔧 Architecture Table

| Component           | Folder / File                         | Purpose                                                         |
| ------------------- | ------------------------------------- | --------------------------------------------------------------- |
| **Main App**        | `main.py`                             | Entry point; initializes and launches the app                   |
| **Core Modules**    | `core/`                               | Contains app logic, error handling, API, GUI setup, and theming |
|                     | `core/app.py`                         | Main app class using `customtkinter`                            |
|                     | `core/api.py`                         | Interfaces with external weather APIs                           |
|                     | `core/processor.py`                   | Extracts and formats weather data                               |
|                     | `core/error_handler.py`               | Graceful handling of missing input or failed API calls          |
|                     | `core/theme.py`                       | Light/Dark theme configuration                                  |
|                     | `core/gui.py`                         | Connects GUI widgets, layout, and styling                       |
| **Feature Modules** | `features/history_tracker/`           | Fetch, process, and show past 7-day weather                     |
|                     | `features/history_tracker/api.py`     | Gets archived weather data from Open-Meteo                      |
|                     | `features/history_tracker/display.py` | Formats history as a table/grid for UI                          |
|                     | `features/history_tracker/geocode.py` | Translates city to lat/lon for history API                      |
|                     | `features/history_tracker/gui.py`     | GUI logic specific to this feature                              |
|                     | `features/extras/`                    | Utility functions and static resources (icons, loaders)         |
| **Data Storage**    | `data/weather_history.csv`            | Stores past weather fetched from API                            |
| **Shared Utils**    | `features/extras/loader.py`           | Loads and resizes weather icons                                 |
| **Cache**           | `__pycache__/`                        | Python bytecode cache (ignored in logic)                        |

### 🔁 Data Flow Overview

User input (city)
      ↓
main.py → core/api.py → weather API
                    ↓
       core/processor.py extracts values
                    ↓
    Sent to GUI modules: core/gui.py + features/gui.py
                    ↓
    Displayed in customtkinter GUI interface
                    ↓
    Data stored in data/weather_history.csv


---------------------------------------------------------------------------------------------------------------------------------------------

## 📊 Section 4: Data Model Plan

| File/Table Name         | Format | Example Row                                               |
| ----------------------- | ------ | --------------------------------------------------------- |
| `weather_history.csv`   | CSV    | `2025-06-09,Delhi,102,Sunny`                              |
| `weather_alerts.txt`    | TXT    | `2025-06-09,Delhi,Heat Warning > 100°F`                   |
| `tomorrow_guess.json`   | JSON   | `{ "city": "Delhi", "date": "2025-06-10", "guess": 101 }` |
| `temperature_graph.csv` | CSV    | `2025-06-03,98\n2025-06-04,100\n2025-06-05,102`           |
| `mood_journal.txt`      | TXT    | `2025-06-09,Delhi,Hot and dry,Feeling drained 😓`         |
| `theme_settings.json`   | JSON   | `{ "theme": "light", "accent": "sunset orange" }`         |

---------------------------------------------------------------------------------------------------------------------------------------------

## 📆 Section 5: Personal Project Timeline

### Week 11

- 🛠 Set up folders, base commit, and repo
- 🔌 Connect core GUI with real-time weather API
- 🎨 Add theme toggle + unit switch (C/F)
- 📊 Start Weather History Tracker (logic & UI)
- ✅ Milestone: Project base + Weather History started

### Week 12

- 🔄 Complete Weather History integration & styling
- 🧪 Test history display, fix layout bugs & icons
- 💾 Store data to CSV and polish inputs
- ✅ Milestone: Feature 1 (History Tracker) done

### Week 13

- ⚠️ Build logic for extreme weather alerts
- 🖼 Design alert UI, add triggers and messages
- ✅ Test and finalize weather alert feature
- ✅ Milestone: Feature 2 (Weather Alerts) done

### Week 14

- 🧹 General UI cleanup and responsiveness
- 🧠 Plan "Tomorrow’s Guess" logic using past trends
- 🧪 Test layout consistency and final touches
- ✅ Milestone: All visuals + layout stable

### Week 15

- 🔮 Build "Tomorrow’s Guess" prediction feature
- 🔗 Integrate with historical data
- 🔧 Debug, polish results, and show estimates
- ✅ Milestone: Feature 3 (Tomorrow’s Guess) done

### Week 16

- 📈 Add temperature graph using matplotlib
- 🌤 Swap icons/emojis for visual polish
- ✨ Optional: Animations or visual extras
- 📚 Write README + setup docs
- ✅ Milestone: Visual + Creative Enhancements done

### Week 17

- 🧪 Final testing and code cleanup
- 🎥 Demo slides, screen recording, and rehearsal
- 🤝 Merge team contributions & final walkthrough
- ✅ Milestone: Demo-ready final project


---------------------------------------------------------------------------------------------------------------------------------------------

## ⚠️ Section 6: Risk Assessment

| Risk                               | Likelihood | Impact | Mitigation Plan                                                          |
| ---------------------------------- | ---------- | ------ | ------------------------------------------------------------------------ |
| API Rate Limit                     | Medium     | Medium | Implement request caching and add delays between API calls               |
| Data Inconsistency                 | Low        | High   | Validate and sanitize API data; handle missing/malformed data gracefully |
| UI Bugs / Theme Issues             | Medium     | Medium | Modularize theme switching; test across themes regularly                 |
| App Slowing Down Laptop            | Medium     | Medium | Optimize image sizes, avoid redundant updates, monitor memory use        |
| Lack of Expertise / Learning Curve | High       | Medium | Break problems down, ask for support early, and build iteratively        |

---------------------------------------------------------------------------------------------------------------------------------------------

## 🤝 Section 7: Support Requests

# | Area of Support              | Description                                                                 |
| ---------------------------- | --------------------------------------------------------------------------- |
| API Data Parsing             | Help troubleshooting edge cases and inconsistent API returns                |
| Matplotlib Integration       | Guidance embedding graphs in a `customtkinter` frame                        |
| GUI Performance Optimization | Help profiling slow updates and reducing CPU load                           |
| Modular File Design          | Review on folder structure, imports, and decoupling GUI from logic          |
| Prediction Logic             | Support building logic for temperature trend guessing                       |
| GitHub Collaboration         | Help resolving merge conflicts and reviewing pull request best practices    |
| Demo Prep                    | Help polishing visuals, arranging layout, and practicing final presentation |


