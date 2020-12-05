from src.visualization import Visualization
from src.population_util import PopulationUtil
from src.config_util import ConfigUtil

class Main(object):
    """
    docstring
    """
    def __init__(self) -> None:
        self.config_util = ConfigUtil("config/config.ini")
        self.load_config()
        self.initialize()

    def load_config(self) -> None:
        self.k                          = self.config_util.getFloatValue("virus.stats", "k_value")
        self.r                          = self.config_util.getFloatValue("virus.stats", "r_value")
        self.size                       = self.config_util.getIntegerValue("area.stats", "total_population")
        self.min_age                    = self.config_util.getIntegerValue("people.stats", "min_age")
        self.max_age                    = self.config_util.getIntegerValue("people.stats", "min_age")
        self.mortality_rate             = self.config_util.getDictionary("virus.stats", "mortality_rate")
        self.social_distance_per        = self.config_util.getFloatValue("people.stats", "social_distancing_percent")
        self.infection_range            = self.config_util.getFloatValue("virus.stats", "infection_range")
        self.recovery_time              = self.config_util.getFloatValue("virus.stats", "recovery_time")
        self.total_healthcare_capacity  = self.size*(self.config_util.getIntegerValue("area.stats", "healthcare_capacity_ratio")/100)
        self.mask_effectiveness         = self.config_util.getDictionary("virus.stats", "mask_effectiveness")
        self.speed                      = self.config_util.getFloatValue("people.stats", "speed")
        self.enforce_social_distance_at = self.config_util.getIntegerValue("area.stats", "enforce_social_distancing_at")
        self.enforce_mask_wearing_at    = self.config_util.getIntegerValue("area.stats", "enforce_mask_wearing_at")

    def initialize(self) -> None:
        self.population_util = PopulationUtil(k = self.k, r = self.r, min_age = self.min_age, max_age = self.max_age, size = self.size,
                                mortality_rate = self.mortality_rate, infection_range = self.infection_range, recovery_time = self.recovery_time,
                                total_healthcare_capacity = self.total_healthcare_capacity, social_distance_per = self.social_distance_per,
                                mask_effectiveness = self.mask_effectiveness, speed=self.speed, social_distancing_at = self.enforce_social_distance_at,
                                mask_wearing_at = self.enforce_mask_wearing_at)
        self.visualize = Visualization(self.population_util, render_mode = False)


if __name__ == "__main__":
    m = Main()
    
