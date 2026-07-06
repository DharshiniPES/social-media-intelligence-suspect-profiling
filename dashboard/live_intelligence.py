import streamlit as st
import pandas as pd

import plotly.express as px
from modules.scrapers.github_scraper import GitHubScraper

from pipeline.intelligence_pipeline import IntelligencePipeline


def show_live_intelligence():

    st.title("Live Intelligence")

    st.caption(
        "Collect OSINT from public sources"
    )

    source = st.selectbox(

        "Source",

        [

            "GitHub",

            "Website",

            "Reddit"

        ]

    )

    target = st.text_input(

        "Target"

    )

    if st.button(

        "Collect Intelligence"

    ):

        if source == "GitHub":

            scraper = GitHubScraper()

            pipeline = IntelligencePipeline()

            github = scraper.scrape(target)

            normalized = pipeline.normalize_github(github)

            evidence = pipeline.run(normalized)

            st.session_state["live_evidence"] = evidence


        elif source == "Website":

            from modules.scrapers.website_scraper import WebsiteScraper

            scraper = WebsiteScraper()

            pipeline = IntelligencePipeline()

            website = scraper.scrape(target)

            normalized = pipeline.normalize_website(website)

            evidence = pipeline.run(normalized)

            st.session_state["live_evidence"] = evidence


        else:

            st.warning("Reddit integration coming soon.")

    if "live_evidence" in st.session_state:

        evidence = st.session_state["live_evidence"]

        profile = evidence["metadata"]

        source = evidence["source"]

        st.success("Collection Complete")

        # =====================================================
        # GITHUB DASHBOARD
        # =====================================================

        if source == "GitHub":

            st.subheader("Executive Overview")

            c1, c2, c3, c4, c5 = st.columns(5)
            with c1:
                st.metric("Emails", len(profile.get("emails", [])))

            with c2:
                st.metric("Phones", len(profile.get("phones", [])))

            with c3:
                st.metric("Internal", len(profile.get("internal_links", [])))

            with c4:
                st.metric("External", len(profile.get("external_links", [])))

            with c5:
                st.metric("Images", len(profile.get("images", [])))

            st.divider()

            left, right = st.columns([2,1])

            with left:

                st.subheader("Profile Intelligence")

                st.write(f"**Username:** {profile.get('username','')}")
                st.write(f"**Name:** {profile.get('name','')}")
                st.write(f"**Company:** {profile.get('company','')}")
                st.write(f"**Location:** {profile.get('location','')}")
                st.write(f"**Website:** {profile.get('blog','')}")
                st.write(f"**Bio:** {profile.get('bio','')}")

            with right:

                if profile.get("avatar"):

                    st.image(
                        profile["avatar"],
                        use_container_width=True
                    )

            st.subheader("AI Intelligence Summary")

            st.info(

                profile.get(

                    "summary",

                    "No summary available."

                )

            )

            st.subheader("Repository Intelligence")

            repos = profile.get("repositories", [])

            repo_table = []

            for repo in repos:

                repo_table.append({

                    "Repository": repo["name"],

                    "Language": repo["language"],

                    "Stars": repo["stars"],

                    "Forks": repo["forks"]

                })

            st.dataframe(

                repo_table,

                use_container_width=True,

                hide_index=True

            )

            languages = {}

            for repo in repos:

                language = repo["language"]

                if language:

                    languages[language] = (

                        languages.get(language, 0) + 1

                    )

            if languages:

                df = pd.DataFrame({

                    "Language": list(languages.keys()),

                    "Repositories": list(languages.values())

                })

                fig = px.pie(

                    df,

                    names="Language",

                    values="Repositories",

                    title="Programming Languages"

                )

                st.plotly_chart(

                    fig,

                    use_container_width=True

                )

            top = sorted(

                repos,

                key=lambda x: x["stars"],

                reverse=True

            )[:10]

            if top:

                df = pd.DataFrame(top)

                fig = px.bar(

                    df,

                    x="name",

                    y="stars",

                    title="Top Starred Repositories"

                )

                st.plotly_chart(

                    fig,

                    use_container_width=True

                )

        # =====================================================
        # WEBSITE DASHBOARD
        # =====================================================

        elif source == "Website":

            st.subheader("Website Intelligence")

            c1, c2, c3 = st.columns(3)

            with c1:

                st.metric(

                    "Emails",

                    len(profile.get("emails", []))

                )

            with c2:

                st.metric(

                    "Phones",

                    len(profile.get("phones", []))

                )

            with c3:

                st.metric(

                    "URLs",

                    len(profile.get("urls", []))

                )

            st.divider()

            st.subheader("Website Information")

            st.write(

                f"**Title:** {profile.get('title','')}"

            )

            st.write(

                f"**Description:** {profile.get('description','')}"

            )

            st.subheader("Visible Text")

            text = profile.get("visible_text", "")

            preview = text[:1200]

            st.text_area(

                "Preview",

                preview,

                height=250

            )

            if len(text) > 1200:

                with st.expander("Show Complete Text"):

                    st.write(text)

            st.subheader("Extracted Intelligence")

            col1, col2 = st.columns(2)

            with col1:

                st.write("### Emails")

                st.write(profile.get("emails", []))

                st.write("### Phones")

                st.write(profile.get("phones", []))

            with col2:

                st.write("### URLs")



                urls = profile.get("urls", [])

                if urls:

                    df = pd.DataFrame({

                        "URL": urls

                    })

                    st.dataframe(

                        df,

                        use_container_width=True,

                        hide_index=True

                    )

                else:

                    st.info("No URLs found.")

                st.write("### Devices")

                st.write(profile.get("devices", []))
            st.subheader("Images")

            images = profile.get("images", [])

            if images:

                cols = st.columns(3)

                for i, img in enumerate(images[:9]):

                    with cols[i % 3]:

                        st.image(

                            img,

                            use_container_width=True

                        )

            else:

                st.info("No images detected.")
            st.subheader("Social Media")

            social = profile.get("social_links", [])

            if social:

                for link in social:

                    st.code(link)

            else:

                st.info("No social media links detected.")
            st.subheader("Technology Stack")

            tech = profile.get("technologies", [])

            if tech:

                cols = st.columns(3)

                for i, t in enumerate(tech):

                    with cols[i % 3]:

                        st.success(t)

            else:

                st.info("No technologies detected.")
            st.subheader("Security Headers")

            security = profile.get("security", {})

            if security:

                rows = []

                for header, present in security.items():

                    rows.append({

                        "Header": header,

                        "Present": "✅" if present else "❌"

                    })

                df = pd.DataFrame(rows)

                st.dataframe(

                    df,

                    use_container_width=True,

                    hide_index=True

                )

            else:

                st.info("No security information available.")
            st.subheader("WHOIS Intelligence")

            whois = profile.get("whois", {})

            if whois:

                rows = []

                for key, value in whois.items():

                    rows.append({

                        "Field": key.replace("_", " ").title(),

                        "Value": value

                    })

                df = pd.DataFrame(rows)

                st.dataframe(

                    df,

                    use_container_width=True,

                    hide_index=True

                )

            else:

                st.info("WHOIS information unavailable.")
            st.subheader("Detected Locations")

            st.write(

                profile.get(

                    "locations",

                    []

                )

            )