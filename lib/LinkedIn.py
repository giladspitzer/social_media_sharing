import SocialMediaAccount


class LinkedIn(SocialMediaAccount):

    def __repr__(self):
        return f"<LinkedIn Account: {self.username}>"

    def validate_account(self):
        # TODO -- use LinkedIn API to validate account exists
        return



