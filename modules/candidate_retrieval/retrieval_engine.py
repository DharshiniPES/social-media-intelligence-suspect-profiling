from modules.username_similarity import username_score
from modules.bio_similarity import bio_score


class CandidateRetrievalEngine:

    @staticmethod
    def retrieve(target, repository_profiles, top_k=100):

        scored = []

        for candidate in repository_profiles:

            # Don't compare a profile to itself
            if (
                target.username == candidate.username
                and target.platform == candidate.platform
            ):
                continue

            # Username similarity
            u_score = username_score(
                target.username,
                candidate.username
            )

            # Bio similarity
            b_score = bio_score(
                target.bio,
                candidate.bio
            )

            # Display name similarity
            display_score = 0

            if (
                target.display_name
                and candidate.display_name
            ):

                display_score = username_score(
                    target.display_name,
                    candidate.display_name
                )

            # Simple retrieval score
            retrieval_score = (
                0.5 * u_score +
                0.3 * display_score +
                0.2 * b_score
            )

            scored.append({

                "candidate": candidate,

                "retrieval_score": retrieval_score

            })

        scored.sort(

            key=lambda x: x["retrieval_score"],

            reverse=True

        )

        return [

            x["candidate"]

            for x in scored[:top_k]

        ]