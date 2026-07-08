import streamlit as st
import pandas as pd
import plotly.express as px

from modules.scrapers.github_scraper import GitHubScraper
from modules.scrapers.website_scraper import WebsiteScraper
from dotenv import load_dotenv




from pipeline.intelligence_pipeline import IntelligencePipeline


def show_live_intelligence():

    st.title("Live Intelligence")

    st.caption(
        "Collect and analyze public intelligence from multiple OSINT sources."
    )

    source = st.selectbox(

        "Source",

        [

            "GitHub",

            "Website",

            "Instagram",

            "Reddit"

        ]

    )

    target = st.text_input(
        "Target"
    )

    if st.button("Collect Intelligence"):

        pipeline = IntelligencePipeline()

        # ---------------------------------------------------------
        # GitHub
        # ---------------------------------------------------------

        if source == "GitHub":

            scraper = GitHubScraper()

            github = scraper.scrape(target)

            normalized = pipeline.normalize_github(github)

            evidence = pipeline.run(normalized)

            st.session_state["live_evidence"] = evidence

        # ---------------------------------------------------------
        # Website
        # ---------------------------------------------------------

        elif source == "Website":

            scraper = WebsiteScraper()

            website = scraper.scrape(target)

            normalized = pipeline.normalize_website(website)

            evidence = pipeline.run(normalized)

            st.session_state["live_evidence"] = evidence

        # ---------------------------------------------------------
        # Instagram
        # ---------------------------------------------------------

        elif source == "Instagram":

            from modules.scrapers.creatorcrawl_instagram import CreatorCrawlInstagram
            from dashboard.instagram_intelligence import InstagramIntelligence

            import os
            
            load_dotenv()
            API_KEY = os.getenv("CREATORCRAWL_API_KEY")

            scraper = CreatorCrawlInstagram(API_KEY)

            profile = scraper.scrape(target)

            profile = InstagramIntelligence().analyze(profile)

            normalized = pipeline.normalize_instagram(
                profile
            )

            evidence = pipeline.run(
                normalized
            )

            st.session_state["live_evidence"] = evidence

        # ---------------------------------------------------------
        # Reddit
        # ---------------------------------------------------------

        else:

            st.warning(
                "Reddit Intelligence will be added in a future update."
            )

    if "live_evidence" not in st.session_state:

        return

    evidence = st.session_state["live_evidence"]

    profile = evidence["metadata"]

    source = evidence["source"]

    st.success("Collection Complete")

    # ==========================================================
    # GITHUB DASHBOARD
    # ==========================================================

    if source == "GitHub":

        st.header("GitHub Intelligence")

        c1, c2, c3, c4, c5 = st.columns(5)

        with c1:
            st.metric(
                "Followers",
                profile.get("followers", 0)
            )

        with c2:
            st.metric(
                "Repositories",
                len(profile.get("repositories", []))
            )

        with c3:
            st.metric(
                "Following",
                profile.get("following", 0)
            )

        with c4:
            st.metric(
                "Public Repos",
                profile.get("public_repos", 0)
            )

        with c5:
            st.metric(
                "Company",
                "Yes" if profile.get("company") else "No"
            )

        st.divider()

        left, right = st.columns([2, 1])

        with left:

            st.subheader("Profile")

            st.write(
                f"**Username:** {profile.get('username','')}"
            )

            st.write(
                f"**Name:** {profile.get('name','')}"
            )

            st.write(
                f"**Company:** {profile.get('company','')}"
            )

            st.write(
                f"**Location:** {profile.get('location','')}"
            )

            st.write(
                f"**Website:** {profile.get('blog','')}"
            )

            st.write(
                f"**Bio:** {profile.get('bio','')}"
            )

        with right:

            if profile.get("avatar"):

                st.image(
                    profile["avatar"],
                    use_container_width=True
                )

        st.subheader("AI Summary")

        st.info(

            profile.get(

                "summary",

                "No summary available."

            )

        )

        repos = profile.get("repositories", [])

        if repos:

            st.subheader("Repositories")

            repo_table = []

            for repo in repos:

                repo_table.append({

                    "Repository": repo.get("name"),

                    "Language": repo.get("language"),

                    "Stars": repo.get("stars"),

                    "Forks": repo.get("forks")

                })

            st.dataframe(

                pd.DataFrame(repo_table),

                use_container_width=True,

                hide_index=True

            )

            languages = {}

            for repo in repos:

                language = repo.get("language")

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

                key=lambda x: x.get("stars", 0),

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

    # ==========================================================
    # WEBSITE DASHBOARD
    # ==========================================================

    elif source == "Website":

        st.header("Website Intelligence")

        c1, c2, c3, c4 = st.columns(4)

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

        with c4:
            st.metric(
                "Images",
                len(profile.get("images", []))
            )

        st.divider()

        left, right = st.columns([2, 1])

        with left:

            st.subheader("Website Information")

            st.write(
                f"**Title:** {profile.get('title','')}"
            )

            st.write(
                f"**Description:** {profile.get('description','')}"
            )

            st.write(
                f"**Risk Score:** {profile.get('risk_score','N/A')}"
            )

        with right:

            technologies = profile.get("technologies", [])

            st.subheader("Technology Stack")

            if technologies:

                for tech in technologies:

                    st.success(tech)

            else:

                st.info("No technologies detected.")

        st.divider()

        st.subheader("Visible Content")

        text = profile.get(
            "visible_text",
            ""
        )

        st.text_area(

            "Preview",

            text[:1500],

            height=250

        )

        if len(text) > 1500:

            with st.expander(
                "Show Complete Text"
            ):

                st.write(text)

        st.divider()

        left, right = st.columns(2)

        with left:

            st.subheader("Emails")

            emails = profile.get("emails", [])

            if emails:

                st.dataframe(

                    pd.DataFrame({

                        "Email": emails

                    }),

                    hide_index=True,

                    use_container_width=True

                )

            else:

                st.info("No emails found.")

            st.subheader("Phones")

            phones = profile.get("phones", [])

            if phones:

                st.dataframe(

                    pd.DataFrame({

                        "Phone": phones

                    }),

                    hide_index=True,

                    use_container_width=True

                )

            else:

                st.info("No phone numbers found.")

        with right:

            st.subheader("URLs")

            urls = profile.get("urls", [])

            if urls:

                st.dataframe(

                    pd.DataFrame({

                        "URL": urls

                    }),

                    hide_index=True,

                    use_container_width=True

                )

            else:

                st.info("No URLs detected.")

            st.subheader("Locations")

            locations = profile.get("locations", [])

            if locations:

                st.dataframe(

                    pd.DataFrame({

                        "Location": locations

                    }),

                    hide_index=True,

                    use_container_width=True

                )

            else:

                st.info("No locations detected.")

        st.divider()

        st.subheader("Social Media Links")

        social = profile.get(
            "social_links",
            []
        )

        if social:

            st.dataframe(

                pd.DataFrame({

                    "Link": social

                }),

                hide_index=True,

                use_container_width=True

            )

        else:

            st.info(
                "No social links detected."
            )

        st.divider()

        st.subheader("Security Headers")

        security = profile.get(
            "security",
            {}
        )

        if security:

            rows = []

            for header, value in security.items():

                rows.append({

                    "Header": header,

                    "Present": "Yes" if value else "No"

                })

            st.dataframe(

                pd.DataFrame(rows),

                hide_index=True,

                use_container_width=True

            )

        else:

            st.info(
                "Security header information unavailable."
            )

        st.subheader("WHOIS Information")

        whois = profile.get("whois", {})

        if whois:

            st.dataframe(

                pd.DataFrame(

                    list(whois.items()),

                    columns=["Field", "Value"]

                ),

                hide_index=True,

                use_container_width=True

            )

        else:

            st.info("WHOIS unavailable.")

        st.subheader("SSL Certificate")

        ssl = profile.get("ssl", {})

        if ssl:

            st.dataframe(

                pd.DataFrame(

                    list(ssl.items()),

                    columns=["Field", "Value"]

                ),

                hide_index=True,

                use_container_width=True

            )

        else:

            st.info("SSL information unavailable.")

        st.subheader("Images")

        images = profile.get(
            "images",
            []
        )

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
    # ==========================================================
    # INSTAGRAM DASHBOARD
    # ==========================================================

    elif source == "Instagram":

        st.header("Instagram Intelligence")

        c1, c2, c3, c4 = st.columns(4)

        with c1:
            st.metric(
                "Followers",
                profile.get("followers", "N/A")
            )

        with c2:
            st.metric(
                "Following",
                profile.get("following", "N/A")
            )

        with c3:
            st.metric(
                "Posts",
                profile.get("posts_count", "N/A")
            )

        with c4:
            st.metric(
                "Intelligence Score",
                profile.get("intelligence_score", 0)
            )

        st.divider()

        left, right = st.columns([2, 1])

        with left:

            st.subheader("Profile Information")

            st.write(f"**Username:** {profile.get('username', '')}")

            st.write(f"**Display Name:** {profile.get('display_name', '')}")

            st.write(f"**Bio:** {profile.get('bio', '')}")

            st.write(f"**Profile URL:** {profile.get('url', '')}")

            st.write(f"**Canonical URL:** {profile.get('canonical_url', '')}")

        with right:
            
            if profile.get("profile_picture"):

                import requests
                from io import BytesIO

                pfp = profile.get("profile_picture")

                if pfp:

                    try:

                        response = requests.get(
                            pfp,
                            headers={
                                "User-Agent": (
                                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                                    "Chrome/138.0 Safari/537.36"
                                ),
                                "Referer": "https://www.instagram.com/"
                            },
                            timeout=20
                        )

                        if response.status_code == 200:
                            st.image(
                                BytesIO(response.content),
                                width=180
                            )
                        else:
                            st.warning("Profile picture unavailable.")

                    except Exception as e:
                        st.warning(e)

        st.divider()

        # ---------------------------------------------------------
        # Recent Posts
        # ---------------------------------------------------------

        st.subheader("Recent Posts")

        posts = profile.get("posts", [])

        if not posts:

            st.info("No recent posts available.")

        else:

            for index, post in enumerate(posts[:10]):

                with st.expander(f"Post {index + 1}", expanded=(index == 0)):

                    media = post.get("media", [])

                    if media:

                        first = media[0]

                        image_url = (
                            first.get("thumbnail_url")
                            or first.get("url")
                        )

                        if image_url:
                            
                            import requests
                            from io import BytesIO

                            try:
                                response = requests.get(
                                    image_url,
                                    headers={
                                        "User-Agent": (
                                            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                                            "AppleWebKit/537.36 (KHTML, like Gecko) "
                                            "Chrome/138.0 Safari/537.36"
                                        ),
                                        "Referer": "https://www.instagram.com/"
                                    },
                                    timeout=20
                                )

                                if response.status_code == 200:
                                    st.image(
                                        BytesIO(response.content),
                                        use_container_width=True
                                    )
                                else:
                                    st.warning(f"Image could not be loaded ({response.status_code})")

                            except Exception as e:
                                st.warning(f"Image Error: {e}")

                    col1, col2, col3 = st.columns(3)

                    with col1:
                        st.metric(
                            "Likes",
                            post.get("like_count", 0)
                        )

                    with col2:
                        st.metric(
                            "Comments",
                            post.get("comment_count", 0)
                        )

                    with col3:
                        st.metric(
                            "Views",
                            post.get("view_count", 0)
                        )

                    st.write(
                        "**Created:**",
                        post.get("created_at", "Unknown")
                    )

                    st.write(
                        "**Type:**",
                        post.get("type", "Unknown")
                    )

                    caption = (
                        post.get("text")
                        or post.get("caption")
                        or ""
                    )

                    if caption:

                        st.write("### Caption")

                        st.write(caption)

        st.divider()

        st.subheader("Metadata")

        col1, col2 = st.columns(2)

        with col1:

            st.write("**Followers**")
            st.info(profile.get("followers", "N/A"))

            st.write("**Following**")
            st.info(profile.get("following", "N/A"))

            st.write("**Posts**")
            st.info(profile.get("posts_count", "N/A"))

        with col2:

            st.write("**Emails**")
            st.write(profile.get("emails", []))

            st.write("**Phones**")
            st.write(profile.get("phones", []))

        st.divider()

        st.subheader("External Domains")

        domains = profile.get("external_domains", [])

        if domains:

            st.dataframe(
                pd.DataFrame({
                    "Domain": domains
                }),
                hide_index=True,
                use_container_width=True
            )

        else:

            st.info("No external domains detected.")

        st.subheader("Risk Indicators")

        risks = profile.get("risk_flags", [])

        if risks:

            st.dataframe(
                pd.DataFrame({
                    "Indicator": risks
                }),
                hide_index=True,
                use_container_width=True
            )

        else:

            st.success("No risk indicators detected.")

        st.divider()

        st.subheader("Pivot Analysis")

        pivots = evidence["analysis"]["pivots"]

        col1, col2 = st.columns(2)

        with col1:

            st.write("### Emails")
            st.write(pivots.get("emails", []))

            st.write("### Phones")
            st.write(pivots.get("phones", []))

            st.write("### URLs")
            st.write(pivots.get("urls", []))

        with col2:

            st.write("### Devices")
            st.write(pivots.get("devices", []))

            st.write("### Locations")
            st.write(pivots.get("locations", []))

        st.divider()

        st.subheader("Metadata")

        metadata = profile.get("metadata", {})

        if metadata:

            rows = []

            for key, value in metadata.items():

                rows.append({
                    "Field": key,
                    "Value": str(value)[:250]
                })

            st.dataframe(
                pd.DataFrame(rows),
                hide_index=True,
                use_container_width=True
            )

        else:

            st.info("No metadata available.")