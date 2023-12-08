import streamlit as st
#make it look nice from the start
st.set_page_config(page_title="VedsuTechonolgy_EventManager", page_icon="📡", layout='wide',initial_sidebar_state='collapsed')
import hydralit_components as hc
import datetime
import Login
import Logout
import Upload
import Home
import History
import Documents
def main():
    # specify the primary menu definition
    menu_data = [
        # {'icon': "far fa-copy", 'label':"Left End"},
        # {'id':'Copy','icon':"🐙",'label':"Copy"},
        {'icon': "fas fa-tachometer-alt", 'label':"Dashboard",'ttip':"I'm the Dashboard tooltip!"}, #can add a tooltip message
        # {'icon': "fa-solid fa-radar",'label':"Dropdown1", 'submenu':[{'id':' subid11','icon': "fa fa-paperclip", 'label':"Sub-item 1"},{'id':'subid12','icon': "💀", 'label':"Sub-item 2"},{'id':'subid13','icon': "fa fa-database", 'label':"Sub-item 3"}]},
        # {'id':' Crazy return value 💀','icon': "💀", 'label':"History"},
        # {'icon': "far fa-arrow-alt-circle-up", 'label':"Upload Doc"},
        {'icon': "far fa-calendar-alt", 'label':"History"},
        {'icon': "far fa-chart-bar", 'label':"Documents"},#no tooltip message
        # x{'icon': "fa-solid fa-radar",'label':"Dropdown2", 'submenu':[{'label':"Sub-item 1", 'icon': "fa fa-meh"},{'label':"Sub-item 2"},{'icon':'🙉','label':"Sub-item 3",}]},
    ]

    over_theme = {'txc_inactive': '#FFFFFF'}
    menu_id = hc.nav_bar(
        menu_definition=menu_data,
        override_theme=over_theme,
        home_name='Home',
        # login_name='Logout',
        hide_streamlit_markers=False, #will show the st hamburger as well as the navbar now!
        sticky_nav=True, #at the top or not
        sticky_mode='pinned', #jumpy or not-jumpy, but sticky or pinned
    )
    if menu_id=='Home':
        # st.info("Home")
        Home.main()
    elif menu_id=='Dashboard':
        # st.info("Dashboard")
        Login.main()
    elif menu_id=='History':
        # st.info('History')
        History.main()
    # elif menu_id=='Upload Doc':
    #     # st.info('Upload Doc')
    #     Upload.main()
    # elif menu_id=='Logout':
    #     # st.info('Logout')
    #     Logout.main()
    elif menu_id=='Documents':
        # st.info('Documents')
        Documents.main()
    


if __name__ == "__main__":
    main()
