import streamlit as st
from datetime import datetime, date
import calendar
import pandas as pd

# ----------------------------------------
# Page Configuration
# ----------------------------------------
st.set_page_config(
    page_title="Personal Organizer",
    page_icon="📅",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ----------------------------------------
# Custom CSS Styling
# ----------------------------------------
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Quicksand:wght@300;400;600;700&display=swap');
        
        * {
            font-family: 'Quicksand', sans-serif;
        }
        
        .main {
            background: linear-gradient(135deg, #faf9f7 0%, #f3ede4 100%);
            min-height: 100vh;
        }
        
        .header-main {
            font-family: 'Playfair Display', serif;
            font-size: 42px;
            font-weight: 700;
            color: #2d2d2d;
            text-align: center;
            margin-bottom: 10px;
            letter-spacing: -1px;
        }
        
        .header-subtitle {
            text-align: center;
            color: #8b7355;
            font-size: 14px;
            margin-bottom: 30px;
            letter-spacing: 1px;
            text-transform: uppercase;
        }
        
        .event-card {
            background: white;
            border-radius: 16px;
            padding: 22px;
            margin: 14px 0;
            box-shadow: 0 6px 20px rgba(45, 45, 45, 0.08);
            border-left: 6px solid #c89a7d;
            transition: all 0.3s cubic-bezier(0.23, 1, 0.320, 1);
            position: relative;
            overflow: hidden;
        }
        
        .event-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 2px;
            background: linear-gradient(90deg, #c89a7d 0%, transparent 100%);
        }
        
        .event-card:hover {
            box-shadow: 0 12px 35px rgba(45, 45, 45, 0.15);
            transform: translateY(-4px);
            border-left-color: #a17f5f;
        }
        
        .event-name {
            font-size: 20px;
            font-weight: 700;
            color: #2d2d2d;
            margin-bottom: 12px;
            font-family: 'Playfair Display', serif;
        }
        
        .event-date {
            display: flex;
            align-items: center;
            gap: 10px;
            color: #666;
            font-size: 14px;
            margin-bottom: 8px;
        }
        
        .date-badge {
            background: linear-gradient(135deg, #e8d5c4 0%, #d9c4b0 100%);
            padding: 8px 14px;
            border-radius: 8px;
            font-weight: 600;
            color: #5a4a3a;
            font-size: 13px;
        }
        
        .input-section {
            background: white;
            border-radius: 16px;
            padding: 28px;
            margin-bottom: 32px;
            box-shadow: 0 6px 20px rgba(45, 45, 45, 0.08);
            border-top: 4px solid #c89a7d;
        }
        
        .section-title {
            font-family: 'Playfair Display', serif;
            font-size: 24px;
            font-weight: 700;
            color: #2d2d2d;
            margin-bottom: 24px;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        
        .stats-card {
            background: white;
            border-radius: 16px;
            padding: 22px;
            text-align: center;
            box-shadow: 0 6px 20px rgba(45, 45, 45, 0.08);
            border-top: 4px solid #c89a7d;
            transition: all 0.3s ease;
        }
        
        .stats-card:hover {
            transform: translateY(-4px);
        }
        
        .stats-number {
            font-size: 36px;
            font-weight: 700;
            color: #c89a7d;
            font-family: 'Playfair Display', serif;
        }
        
        .stats-label {
            font-size: 13px;
            color: #8b7355;
            margin-top: 8px;
            letter-spacing: 0.5px;
            text-transform: uppercase;
        }
        
        .month-year {
            font-family: 'Playfair Display', serif;
            font-size: 20px;
            color: #2d2d2d;
            text-align: center;
            margin-bottom: 20px;
            font-weight: 700;
        }
        
        .calendar-container {
            background: white;
            border-radius: 16px;
            padding: 24px;
            box-shadow: 0 6px 20px rgba(45, 45, 45, 0.08);
            margin-bottom: 32px;
        }
        
        .calendar-grid {
            display: grid;
            grid-template-columns: repeat(7, 1fr);
            gap: 8px;
            margin-top: 16px;
        }
        
        .calendar-day-header {
            text-align: center;
            font-weight: 600;
            color: #c89a7d;
            font-size: 12px;
            text-transform: uppercase;
            padding: 8px;
            letter-spacing: 1px;
        }
        
        .calendar-day {
            aspect-ratio: 1;
            display: flex;
            align-items: center;
            justify-content: center;
            border-radius: 8px;
            background: #faf9f7;
            color: #666;
            font-size: 13px;
            cursor: pointer;
            transition: all 0.2s ease;
            font-weight: 500;
        }
        
        .calendar-day:hover {
            background: #e8d5c4;
            color: #2d2d2d;
            transform: scale(1.05);
        }
        
        .calendar-day-empty {
            background: transparent;
            cursor: default;
        }
        
        .calendar-day-empty:hover {
            background: transparent;
            transform: none;
        }
        
        .calendar-day.has-event {
            background: linear-gradient(135deg, #c89a7d 0%, #a17f5f 100%);
            color: white;
            font-weight: 700;
        }
        
        .calendar-day.has-event:hover {
            background: linear-gradient(135deg, #a17f5f 0%, #8b6a4f 100%);
        }
        
        .filter-section {
            display: flex;
            gap: 12px;
            margin-bottom: 20px;
            flex-wrap: wrap;
        }
        
        .empty-state {
            text-align: center;
            padding: 60px 20px;
            color: #8b7355;
        }
        
        .empty-state-icon {
            font-size: 56px;
            margin-bottom: 16px;
        }
        
        .empty-state-title {
            font-family: 'Playfair Display', serif;
            font-size: 22px;
            color: #2d2d2d;
            margin-bottom: 8px;
        }
    </style>
""", unsafe_allow_html=True)

# ----------------------------------------
# Initialize Session State
# ----------------------------------------
if 'eventName' not in st.session_state:
    st.session_state.eventName = []
    st.session_state.eventMonth = []
    st.session_state.eventDay = []
    st.session_state.eventYear = []
    st.session_state.eventCreated = []

# ----------------------------------------
# Validation Functions
# ----------------------------------------
def validateMonth(month):
    """Validate month is between 1 and 12"""
    try:
        month_int = int(month)
        if 1 <= month_int <= 12:
            return month_int, True
        return None, False
    except ValueError:
        return None, False

def validateDay(month, day, year):
    """Validate day based on month and year"""
    try:
        day_int = int(day)
        month_int = int(month)
        year_int = int(year)
        
        # Determine number of days in the month
        if month_int == 2:
            # Leap year check
            if (year_int % 4 == 0 and year_int % 100 != 0) or (year_int % 400 == 0):
                max_days = 29
            else:
                max_days = 28
        elif month_int in [4, 6, 9, 11]:
            max_days = 30
        else:
            max_days = 31
        
        if 1 <= day_int <= max_days:
            return day_int, True
        return None, False
    except ValueError:
        return None, False

def validateYear(year):
    """Validate year is reasonable"""
    try:
        year_int = int(year)
        if 1900 <= year_int <= 2100:
            return year_int, True
        return None, False
    except ValueError:
        return None, False

def addEvent(name, month, day, year):
    """Add event to session state"""
    if not name.strip():
        return False, "Event name cannot be empty"
    
    month_valid, is_valid = validateMonth(month)
    if not is_valid:
        return False, "Month must be between 1 and 12"
    
    year_valid, is_valid = validateYear(year)
    if not is_valid:
        return False, "Year must be between 1900 and 2100"
    
    day_valid, is_valid = validateDay(month_valid, day, year_valid)
    if not is_valid:
        max_days = 31
        if month_valid == 2:
            if (year_valid % 4 == 0 and year_valid % 100 != 0) or (year_valid % 400 == 0):
                max_days = 29
            else:
                max_days = 28
        elif month_valid in [4, 6, 9, 11]:
            max_days = 30
        return False, f"Day must be between 1 and {max_days} for this month"
    
    st.session_state.eventName.append(name)
    st.session_state.eventMonth.append(month_valid)
    st.session_state.eventDay.append(day_valid)
    st.session_state.eventYear.append(year_valid)
    st.session_state.eventCreated.append(datetime.now().strftime("%H:%M:%S"))
    return True, "Event added successfully!"

def deleteEvent(index):
    """Delete event by index"""
    st.session_state.eventName.pop(index)
    st.session_state.eventMonth.pop(index)
    st.session_state.eventDay.pop(index)
    st.session_state.eventYear.pop(index)
    st.session_state.eventCreated.pop(index)

def getMonthName(month_num):
    """Get month name from number"""
    months = ["January", "February", "March", "April", "May", "June",
              "July", "August", "September", "October", "November", "December"]
    return months[month_num - 1] if 1 <= month_num <= 12 else "Unknown"

def getEventsByMonthYear(month, year):
    """Get events for a specific month and year"""
    events = []
    for i, (m, d, y, name) in enumerate(zip(st.session_state.eventMonth, 
                                             st.session_state.eventDay,
                                             st.session_state.eventYear,
                                             st.session_state.eventName)):
        if m == month and y == year:
            events.append((i, d, name))
    return sorted(events, key=lambda x: x[1])

def getUpcomingEvents(limit=5):
    """Get upcoming events sorted by date"""
    events = []
    today = datetime.now()
    
    for i, (name, m, d, y) in enumerate(zip(st.session_state.eventName,
                                             st.session_state.eventMonth,
                                             st.session_state.eventDay,
                                             st.session_state.eventYear)):
        try:
            event_date = datetime(y, m, d)
            if event_date >= today:
                events.append((i, event_date, name, m, d, y))
        except:
            pass
    
    return sorted(events, key=lambda x: x[1])[:limit]

# ----------------------------------------
# Header
# ----------------------------------------
st.markdown("<div class='header-main'>📅 Personal Organizer</div>", unsafe_allow_html=True)
st.markdown("<div class='header-subtitle'>Manage Your Events & Schedule</div>", unsafe_allow_html=True)

# ----------------------------------------
# Statistics
# ----------------------------------------
if st.session_state.eventName:
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
            <div class='stats-card'>
                <div class='stats-number'>{len(st.session_state.eventName)}</div>
                <div class='stats-label'>Total Events</div>
            </div>
        """, unsafe_allow_html=True)
    
    upcoming = len(getUpcomingEvents(1000))
    with col2:
        st.markdown(f"""
            <div class='stats-card'>
                <div class='stats-number'>{upcoming}</div>
                <div class='stats-label'>Upcoming</div>
            </div>
        """, unsafe_allow_html=True)
    
    this_year = sum(1 for y in st.session_state.eventYear if y == datetime.now().year)
    with col3:
        st.markdown(f"""
            <div class='stats-card'>
                <div class='stats-number'>{this_year}</div>
                <div class='stats-label'>This Year</div>
            </div>
        """, unsafe_allow_html=True)
    
    this_month = sum(1 for m, y in zip(st.session_state.eventMonth, st.session_state.eventYear) 
                     if m == datetime.now().month and y == datetime.now().year)
    with col4:
        st.markdown(f"""
            <div class='stats-card'>
                <div class='stats-number'>{this_month}</div>
                <div class='stats-label'>This Month</div>
            </div>
        """, unsafe_allow_html=True)

st.markdown("---")

# ----------------------------------------
# Add Event Section
# ----------------------------------------
st.markdown("<div class='input-section'>", unsafe_allow_html=True)
st.markdown("<div class='section-title'>✨ Add New Event</div>", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    event_name = st.text_input("Event Name", placeholder="Enter event name...")

with col2:
    event_month = st.selectbox("Month", list(range(1, 13)), 
                               format_func=lambda x: getMonthName(x))

with col3:
    event_day = st.number_input("Day", min_value=1, max_value=31, value=1)

with col4:
    event_year = st.number_input("Year", min_value=1900, max_value=2100, 
                                 value=datetime.now().year)

col_add, col_space = st.columns([1, 4])
with col_add:
    if st.button("➕ Add Event", use_container_width=True, key="add_event_btn"):
        success, message = addEvent(event_name, event_month, event_day, event_year)
        if success:
            st.success(message)
            st.rerun()
        else:
            st.error(message)

st.markdown("</div>", unsafe_allow_html=True)

st.markdown("---")

# ----------------------------------------
# Tabs for different views
# ----------------------------------------
tab1, tab2, tab3 = st.tabs(["📋 All Events", "📅 Calendar View", "⏰ Upcoming"])

# ----------------------------------------
# Tab 1: All Events
# ----------------------------------------
with tab1:
    if st.session_state.eventName:
        st.markdown("<div class='section-title'>All Events</div>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            sort_by = st.selectbox("Sort by", ["Date (Newest)", "Date (Oldest)", "Alphabetical"],
                                  key="sort_all")
        with col2:
            search_term = st.text_input("Search events", placeholder="Search by name...", key="search_all")
        
        # Filter and sort
        display_indices = []
        for i, name in enumerate(st.session_state.eventName):
            if search_term.lower() in name.lower():
                display_indices.append(i)
        
        # Sort
        if sort_by == "Date (Newest)":
            display_indices.sort(key=lambda i: (st.session_state.eventYear[i], 
                                               st.session_state.eventMonth[i], 
                                               st.session_state.eventDay[i]), reverse=True)
        elif sort_by == "Date (Oldest)":
            display_indices.sort(key=lambda i: (st.session_state.eventYear[i], 
                                               st.session_state.eventMonth[i], 
                                               st.session_state.eventDay[i]))
        else:  # Alphabetical
            display_indices.sort(key=lambda i: st.session_state.eventName[i])
        
        # Display events
        for idx in display_indices:
            col1, col2, col3 = st.columns([4, 1, 0.5])
            
            with col1:
                month_name = getMonthName(st.session_state.eventMonth[idx])
                date_str = f"{month_name} {st.session_state.eventDay[idx]}, {st.session_state.eventYear[idx]}"
                
                st.markdown(f"""
                    <div class='event-card'>
                        <div class='event-name'>{st.session_state.eventName[idx]}</div>
                        <div class='event-date'>
                            <span class='date-badge'>📆 {date_str}</span>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.write("")
            
            with col3:
                if st.button("🗑", key=f"delete_all_{idx}", help="Delete event"):
                    deleteEvent(idx)
                    st.rerun()
    else:
        st.markdown("""
            <div class='empty-state'>
                <div class='empty-state-icon'>📭</div>
                <div class='empty-state-title'>No Events Yet</div>
                <p>Create your first event using the form above to get started!</p>
            </div>
        """, unsafe_allow_html=True)

# ----------------------------------------
# Tab 2: Calendar View
# ----------------------------------------
with tab2:
    st.markdown("<div class='section-title'>Calendar View</div>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        cal_month = st.selectbox("Month", list(range(1, 13)), 
                                format_func=lambda x: getMonthName(x),
                                key="cal_month")
    with col2:
        cal_year = st.number_input("Year", min_value=1900, max_value=2100, 
                                  value=datetime.now().year, key="cal_year")
    
    st.markdown(f"<div class='calendar-container'>", unsafe_allow_html=True)
    st.markdown(f"<div class='month-year'>{getMonthName(cal_month)} {cal_year}</div>", unsafe_allow_html=True)
    
    # Create calendar
    cal = calendar.monthcalendar(cal_year, cal_month)
    month_events = getEventsByMonthYear(cal_month, cal_year)
    event_days = {d: name for _, d, name in month_events}
    
    # Days of week header
    cols = st.columns(7)
    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    for col, day in zip(cols, days):
        col.markdown(f"<div class='calendar-day-header'>{day}</div>", unsafe_allow_html=True)
    
    # Calendar days
    for week in cal:
        cols = st.columns(7)
        for col, day in zip(cols, week):
            if day == 0:
                col.markdown("<div class='calendar-day calendar-day-empty'></div>", unsafe_allow_html=True)
            elif day in event_days:
                col.markdown(f"<div class='calendar-day has-event' title='{event_days[day]}'>{day}</div>", 
                           unsafe_allow_html=True)
            else:
                col.markdown(f"<div class='calendar-day'>{day}</div>", unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Show events for selected month
    if month_events:
        st.markdown("#### Events this month:")
        for idx, day, name in month_events:
            col1, col2 = st.columns([4, 0.5])
            with col1:
                st.markdown(f"**{day}** - {name}")
            with col2:
                if st.button("🗑", key=f"delete_cal_{idx}", help="Delete event"):
                    deleteEvent(idx)
                    st.rerun()

# ----------------------------------------
# Tab 3: Upcoming Events
# ----------------------------------------
with tab3:
    st.markdown("<div class='section-title'>Upcoming Events</div>", unsafe_allow_html=True)
    
    upcoming = getUpcomingEvents(1000)
    
    if upcoming:
        for idx, event_date, name, m, d, y in upcoming:
            days_until = (event_date.date() - datetime.now().date()).days
            
            if days_until == 0:
                time_label = "🔴 Today!"
            elif days_until == 1:
                time_label = "🟠 Tomorrow"
            elif days_until < 7:
                time_label = f"🟡 In {days_until} days"
            elif days_until < 30:
                time_label = f"🟢 In {days_until // 7} weeks"
            else:
                time_label = f"🔵 In {days_until // 30} months"
            
            col1, col2, col3 = st.columns([4, 1, 0.5])
            
            with col1:
                month_name = getMonthName(m)
                st.markdown(f"""
                    <div class='event-card'>
                        <div class='event-name'>{name}</div>
                        <div class='event-date'>
                            <span class='date-badge'>📆 {month_name} {d}, {y}</span>
                            <span style='color: #c89a7d; font-weight: 600;'>{time_label}</span>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.write("")
            
            with col3:
                if st.button("🗑", key=f"delete_upcoming_{idx}", help="Delete event"):
                    deleteEvent(idx)
                    st.rerun()
    else:
        st.markdown("""
            <div class='empty-state'>
                <div class='empty-state-icon'>🎉</div>
                <div class='empty-state-title'>No Upcoming Events</div>
                <p>Great! You have no upcoming events. Add one to get started!</p>
            </div>
        """, unsafe_allow_html=True)

# ----------------------------------------
# Footer
# ----------------------------------------
st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: #8b7355; font-size: 12px; padding: 20px;'>
        Personal Organizer © 2025 | Built with Streamlit
    </div>
""", unsafe_allow_html=True)
