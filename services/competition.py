from repository.competition import Competition


class CompetitionService():
    def __init__(self) -> None:
        self.competitions = Competition.load_competitions()

    def get_competition_by_name(self, name):
        return [comp for comp in self.competitions if comp['name'] == name][0]
