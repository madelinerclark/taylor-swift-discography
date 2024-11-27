import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import pandas as pd
import streamlit as st
import sqlite3 as sql
from matplotlib import rcParams

from src import charts
from src import streamlit_mods
from src import toolkit

st.set_page_config(page_title='Genius Page Views')

connection = sql.connect('data/taylor_swift.db')
cursor = connection.cursor()

eras = toolkit.eras_order()

rcParams, custom_params = toolkit.chart_params(rcParams)

# Creating temporary table to be used throughout
temp_table = toolkit.sql_to_string('views_temp_table.sql')
cursor.executescript(temp_table)

streamlit_mods.increase_width()

def main():
    streamlit_mods.get_sidebar()
    content()

@st.cache_data
def content():
    st.markdown("""
    ## Genius Page Views

    Genius is a premiere hub for song lyrics and lyrical analysis, and with Taylor Swift's autobiographical lyrics having extended metaphors and purple prose, it's not surprising that many of Taylor's songs get traffic on Genius. I want to see which albums or overall song eras get the most attention on Genius based on the traffic that each album/era's individual song gets. I use two approaches to answer this query:

    1. I total the number of page views for each song and compare them to one another to see which is the most popular, as well as plot the frequency distribution of page views across Taylor's discography.
    2. I plot the distribution of page views via a boxplot to compare the medians, means, and any outliers that potentially influence the previous approach's conclusions.
    """)
    df_views = pd.read_sql('SELECT * FROM song_views', connection)
    
    views_totals = toolkit.sql_to_string('views_totals.sql')
    era_views = pd.read_sql(views_totals, connection)
    toolkit.abbreviate_ttpd(era_views['era'])
    toolkit.abbreviate_ttpd(df_views['era'])
    toolkit.sort_cat_column(era_views, 'era', eras)
    toolkit.sort_cat_column(df_views, 'era', eras)

    views_fig, views_ax = charts.views_plots(custom_params, era_views, 'total_views', 'era', df_views, 'views', 
                                             'Song Page Views on Genius', 'Total Page Views per Era', 'Frequency Distribution of Page Views',
                                             'Total Page Views', 'Page Views', 'Album/Song Era', 'Song Count', ['#858ae3', '#613dc1'], 
                                             ['#4e148c', '#2c0735'], True, 'total_page_views_distribution.png')
    st.pyplot(views_fig)

    with st.expander('See discussion'):
        st.write("""
            Despite being the most recently released album, *The Tortured Poets Department* has taken the lead at nearly 54.3 million total page views, which is over 25 million more page views than *folklore* has in second place. *Midnights* is in third place with 24.8 million and *Lover* in fouth with 20.8 million views. From her studio albums, her debut *Taylor Swift* has the least amount of views at 2.4 million, with her song collaborations with other artists being just above that at 2.8 million total views. Of her rerecordings, *Red (Taylor's Version)* is the most popular with 10.9 million views, while *Fearless (Taylor's Version)* is the least popular at 3.6 million views. It's possible to conclude from this graph that *The Tortured Poets Department* is Taylor Swift's most popular album on Genius in terms of traffic to the album's songs.

            There are a few problems with this approach, as illustrated by the accompanying histogram: the data is skewed to the right, with most song pages having under 1 million views. Because of this, these totals are most likely influenced by outliers, or individual songs with high amounts of views. To counteract that, we plot the distributions and see how the medians compare to one another.
            """)

    view_box_fig, view_box_ax = charts.views_box(custom_params, df_views,'views', 'era', 'Genius Song Page View Distribution per Album/Song Category', 
                                                 'Page Views', 'Album/Song Era', '#7D7C78', '#3A3633', True, 'page_view_box_distribution.png')
    st.pyplot(view_box_fig)

    with st.expander('See discussion'):
        st.write("""
            All of Taylor's eras are influenced in some capacity by outliers in terms of page views; all of their means (represented by white dots) fall to the right of their medians (represented by the vertical bars in the boxes). The most egregious example is *Red (Taylor's Version),* whose song "All Too Well (10 Minute Version) (Taylor’s Version) [From The Vault]" is the most viewed Taylor Swift song on Genius at 5.4 million views, making up nearly half of its calculated page view totals from the previous visualization.

            Looking at medians, *The Tortured Poets Department*  has the highest at around 1.6 million followed by *folklore* at around 1.4 million, meaning on average songs from both *folklore* and *The Tortured Poets Department* get more page views than songs from other albums or eras. With this statistic, we can argue that *The Tortured Poets Department* is the most popular Taylor Swift album on Genius with *folklore* in second place, which matches the conclusion of the previous approach. However, *reputation* has the third highest median of around 1.1 million views per song page, which differs from the first approach having *reputation* being the sixth most popular at 18 million total page views. This means that songs from *reputation* on average get more page views than other song pages from different albums/eras, even if the total for the album is lower overall.

            In terms of lowest medians, all four of Taylor's rercorded albums have very low median views-per-page, each having around 0.1 million (100,000) per song, and all rerecorded albums have lower medians than their original counterparts. This could be due to how recently the albums were released, as the original albums have existed on Genius for much longer, but in my opinion it's more likely that Genius suggests the song pages from the original albums more often than it does for their rerecorded counterparts when the user searches for the song title. The only era that is lower than the rerecorded albums is Taylor's non-album songs, such as movie soundtrack releases or promotional singles, which have the lowest median views-per-page.
            """)

if __name__ == '__main__':
    main()

connection.close()