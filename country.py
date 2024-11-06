from __future__ import annotations

from typing import TYPE_CHECKING, List, Optional

from plotting_utilities import plot_country, plot_path

import math
import warnings

if TYPE_CHECKING:
    from pathlib import Path

    from matplotlib.figure import Figure


def travel_time(
    distance,
    different_regions,
    locations_in_dest_region,
    speed,
):
    travel_time = distance / (3600 * speed) *(1+(different_regions * locations_in_dest_region)/10)
    return travel_time


class Location:
    def __repr__(self):
        """
        Do not edit this function.
        You are NOT required to document or test this function.

        Not all methods of printing variable values delegate to the
        __str__ method. This implementation ensures that they do,
        so you don't have to worry about Locations not being formatted
        correctly due to these internal Python caveats.
        """
        return self.__str__()

    def __str__(self):
        if self.settlement:
            label = "settlement"
        else:
            label = "depot"
        
        theta_over_pi = self.theta / math.pi

        return f"{self.name} [{label}] in {self.region} @ ({self.r:.2f} m, {theta_over_pi:.2f} pi) "

    def distance_to(self, other):
        distance = math.sqrt(self.r ** 2 + other.r ** 2 - 2 * self.r * other.r * math.cos(self.theta - other.theta) )
        return distance

    def capitalize_string(self, input_string):
       
        capitalized_string = input_string.title()  # Capitalize each word
        if capitalized_string != input_string:
            warnings.warn(f"The string '{input_string}' was updated to '{capitalized_string}'.")
        return capitalized_string
    def __init__(self, name, region, r, theta, depot):
        if not isinstance(name, str):
            raise TypeError("Name should be a string.")
         
        if not isinstance(region, str):
            raise TypeError("Region should be a string.")
         
        self.name = self.capitalize_string(name)
        self.region = self.capitalize_string(region)
    
        try:
            self.r = float(r)
        except ValueError:
            raise ValueError ("Polar radius(r) must be a number.")

        if self.r < 0:
            raise ValueError("Polar radius(r) must be non-negative.")
    
        try:
            self.theta = float(theta)
        except ValueError:
            raise ValueError ("Polar angle(theta) must be a number.")

        if self.theta < -math.pi or self.theta > math.pi:
            raise ValueError("Polar angle(theta) must be between {-math.pi} and {math.pi}.")

        if not isinstance(depot, bool):
            raise TypeError("Depot flag must be a boolean.")
        
        self.depot = depot

    @property
    def settlement(self):
        return not self.depot


class Country:

    def travel_time(self, start_location, end_location):
        raise NotImplementedError

    def fastest_trip_from(
        self,
        current_location,
        potential_locations,
    ):
        raise NotImplementedError

    def nn_tour(self, starting_depot):
        raise NotImplementedError

    def best_depot_site(self, display):
        raise NotImplementedError

    def plot_country(
        self,
        distinguish_regions: bool = True,
        distinguish_depots: bool = True,
        location_names: bool = True,
        polar_projection: bool = True,
        save_to: Optional[Path | str] = None,
    ) -> Figure:
        """

        Plots the locations that make up the Country instance on a
        scale diagram, either displaying or saving the figure that is
        generated.

        Use the optional arguments to change the way the plot displays
        the information.

        Attention
        ---------
        You are NOT required to write tests or documentation for this
        function; and you are free to remove it from your final
        submission if you wish.

        You should remove this function from your submission if you
        choose to delete the plotting_utilities.py file.

        Parameters
        ----------
        distinguish_regions : bool, default: True
            If True, locations in different regions will use different
            marker colours.
        distinguish_depots bool, default: True
            If True, depot locations will be marked with crosses
            rather than circles.  Their labels will also be in
            CAPITALS, and underneath their markers, if not toggled
            off.
        location_names : bool, default: True
            If True, all locations will be annotated with their names.
        polar_projection : bool, default: True
            If True, the plot will display as a polar
            projection. Disable this if you would prefer the plot to
            be displayed in Cartesian (x,y) space.
        save_to : Path, str
            Providing a file name or path will result in the diagram
            being saved to that location. NOTE: This will suppress the
            display of the figure via matplotlib.
        """
        return plot_country(
            self,
            distinguish_regions=distinguish_regions,
            distinguish_depots=distinguish_depots,
            location_names=location_names,
            polar_projection=polar_projection,
            save_to=save_to,
        )

    def plot_path(
        self,
        path: List[Location],
        distinguish_regions: bool = True,
        distinguish_depots: bool = True,
        location_names: bool = True,
        polar_projection: bool = True,
        save_to: Optional[Path | str] = None,
    ) -> Figure:
        """
        Plots the path provided on top of a diagram of the country,
        in order to visualise the path.

        Use the optional arguments to change the way the plot displays
        the information. Refer to the plot_country method for an
        explanation of the optional arguments.

        Attention
        ---------
        You are NOT required to write tests or documentation for this
        function; and you are free to remove it from your final
        submission if you wish.

        You should remove this function from your submission if you
        choose to delete the plotting_utilities.py file.

        Parameters
        ----------
        path : list
            A list of Locations in the country, where consecutive
            pairs are taken to mean journeys from the earlier location to
            the following one.
        distinguish_regions : bool, default: True,
        distinguish_depots : bool, default: True,
        location_names : bool, default: True,
        polar_projection : bool, default: True,
        save_to : Path, str

        See Also
        --------
        self.plot_path for a detailed description of the parameters
        """
        return plot_path(
            self,
            path,
            distinguish_regions=distinguish_regions,
            distinguish_depots=distinguish_depots,
            location_names=location_names,
            polar_projection=polar_projection,
            save_to=save_to,
        )
