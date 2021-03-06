'''
Created on Jan 29, 2020
@author: manik
'''

from matplotlib.pyplot import margins
from src.population_util import PopulationUtil  
from matplotlib import gridspec
import matplotlib.pyplot as plt
import src.person_properties_util as index
import numpy as np
from matplotlib.animation import FuncAnimation
import matplotlib as mpl
import sys
import networkx as nx
import matplotlib.patches as mpatches

class Visualization():

    def __init__(self, population_util: PopulationUtil, render_mode: bool = False, render_path: str ="render"):
        """
        Constructor to set the population_util, render_mode and path, and initialize figure

        Parameters
        ----------
        :param population_util: PopulationUtil object using which we will run the visualization backend.
        :param render_mode: Toggle to switch to render mode from animation mode.
        :param render_path: Path to where render should be stored.
        """

        self.putil = population_util

        # Disable toolbar
        mpl.rcParams['toolbar'] = 'None' 

        # Initialize figure
        self.fig = plt.figure(figsize=(6.5,7.5))
        self.fig.canvas.set_window_title('Simulation')

        # Initialize 3 subplots
        spec = gridspec.GridSpec(ncols=1, nrows=3,height_ratios=[2, 1, 0.5])
        self.ax = self.fig.add_subplot(spec[0])
        self.ax1 = self.fig.add_subplot(spec[1])
        self.ax2 = self.fig.add_subplot(spec[2])

        # Set X and Y limits and other settings on subplots
        self.ax.set_xlim(self.putil.x_bounds[0] , self.putil.x_bounds[1])
        self.ax.set_ylim(self.putil.y_bounds[0] , self.putil.y_bounds[1])
        self.ax1.set_xlim(0 , 1000)
        self.ax1.set_ylim(0 , self.putil.size)
        self.ax.axis('off')
        self.ax2.axis('off')

        # Initialize the animation
        self.ani = FuncAnimation(self.fig, self.update, interval=5, init_func=self.setup_plot, blit=False)

        # If render mode, reinitialize.
        if render_mode == True:
            self.ani = FuncAnimation(self.fig, self.update, interval=5, frames=1000, init_func=self.setup_plot, blit=False)
            render_path = render_path + "/render.mp4"
            print("Rendering to " + render_path, file = sys.stdout)
            self.ani.save(render_path, fps=30, dpi=120)
            print("Render Completed", file = sys.stdout)
        # Show animation.
        else:
            plt.show()

            # Create a digraph showing the infection spread
            fig = plt.figure()
            G = nx.Graph()
            color_map = []
            size_map = []

            # Label Patches
            red_patch = mpatches.Patch(color='red', label='First Infection')
            blue_patch = mpatches.Patch(color='cornflowerblue', label='Infected But Recovered')
            indigo_patch = mpatches.Patch(color='indigo', label='Dead')
            orange_patch = mpatches.Patch(color='orange', label='Currently Infected')
            plt.legend(handles=[red_patch, blue_patch, indigo_patch, orange_patch])

            # Adding graphs edges
            for i in range(self.putil.size):
                if(self.putil.population.persons[i, index.infected_by] != i and self.putil.population.persons[i, index.infected_by] != -1): 
                    if(self.putil.population.persons[i, index.current_state] == 2):
                        G.add_edge(i,self.putil.population.persons[i, index.infected_by])
                        color_map.append('cornflowerblue')
                        size_map.append(15)
                    elif(self.putil.population.persons[i, index.current_state] == 3):
                        G.add_edge(i,self.putil.population.persons[i, index.infected_by])
                        color_map.append('indigo')
                        size_map.append(15)
                    else:
                        G.add_edge(i,self.putil.population.persons[i, index.infected_by])
                        color_map.append('orange')
                        size_map.append(15)
                elif(self.putil.population.persons[i, index.infected_by] == i):
                    G.add_node(i)
                    color_map.append('red')
                    size_map.append(50)
            
            # Show graph
            nx.draw_spring(G, node_size = size_map, node_color = color_map, edge_color = 'darkgray')
            fig.canvas.set_window_title('Infection Tracing Visualization')
            plt.show()

    def setup_plot(self):
        """
        Method to setup how the initial plot and visualization looks like

        Returns
        -------
        :returns Variables that store plot objects
        """

        # Get all the healthy, immune, infected, and dead people seperately 
        healthy_x = self.putil.population.get_all_healthy()[:, index.x_axis]
        healthy_y = self.putil.population.get_all_healthy()[:, index.y_axis]
        infected_x = self.putil.population.get_all_infected()[:, index.x_axis]
        infected_y = self.putil.population.get_all_infected()[:, index.y_axis]
        immune_x = self.putil.population.get_all_recovered()[:, index.x_axis]
        immune_y = self.putil.population.get_all_recovered()[:, index.y_axis]
        dead_x = self.putil.population.get_all_dead()[:, index.x_axis]
        dead_y = self.putil.population.get_all_dead()[:, index.y_axis]
        total_infected = self.putil.size - len(healthy_x)
        total_hospitalized = len(self.putil.persons[self.putil.persons[:,index.hospitalized] == 3])
        
        # Current healthcare status
        self.healthcare_status   = "Normal"
        
        # Scatter plots to plot people
        self.scat = self.ax.scatter(healthy_x,
                                        healthy_y, vmin=0, vmax=1,
                                                cmap="jet", c="lightsteelblue", s=10)
        self.scat2 = self.ax.scatter(infected_x,
                                        infected_y, vmin=0, vmax=1,
                                                cmap="jet", c="indianred", s=10)
        self.scat3 = self.ax.scatter(immune_x,
                                        immune_y, vmin=0, vmax=1,
                                                cmap="jet", c="mediumseagreen", s=10)
        self.scat4 = self.ax.scatter(dead_x,
                                        dead_y, vmin=0, vmax=1,
                                                cmap="jet", c="indigo", s=10)
        # Lists for line graph
        self.infected       = []
        self.infected_total = []
        self.deaths         = []
        self.frames         = []
        self.immunes        = []
        self.infected.append(len(infected_x))
        self.deaths.append(len(dead_x))
        self.infected_total.append(self.putil.size - len(healthy_x))
        self.immunes.append(len(immune_x))
        self.frames.append(0)

        # Line graph plotting number
        self.total_infected,     = self.ax1.plot(self.frames, self.infected_total)
        self.currently_infected, = self.ax1.plot(self.frames, self.infected, c="indianred", label='Currently Infected')
        self.total_deaths,       = self.ax1.plot(self.frames, self.deaths, c="indigo", label='Total Dead')
        self.total_immune,       = self.ax1.plot(self.frames, self.immunes, c="mediumseagreen", label='Total Immune')

        # Code below prints statistics 
        if(self.putil.enforce_social_distance_at > 0):
            self.ax1.plot([self.putil.enforce_social_distance_at]*2, [0,self.putil.size],c="gold", label="Social Distancing")
            self.social_distancing_info = ("At frame " + str(self.putil.enforce_social_distance_at))
            self.social_distancing_num = str(int(self.putil.social_distance_per * self.putil.size)) + " or " + str(self.putil.social_distance_per*100)+"%"
        else:
            self.social_distancing_info = ("Disabled")
            self.social_distancing_num = "0 or 0%"

        if(self.putil.enforce_mask_wearing_at > 0):
            self.ax1.plot([self.putil.enforce_mask_wearing_at]*2, [0,self.putil.size],c="hotpink", label="Mask Mandate")
            self.mask_wearing_info = "At frame " + str(self.putil.enforce_mask_wearing_at) 
        else:
            self.mask_wearing_info = "Disabled"

        self.ax1.tick_params(axis="y",direction="in", pad=3)
        self.ax1.plot([0,1000],[self.putil.virus.total_healthcare_capacity]*2, c="silver")
        self.ax1.get_xaxis().set_visible(False)
        self.ax1.legend(prop={'size': 8},loc='upper right')
        self.ax2.text(0,1,"Statistics", fontsize='large' , fontweight='bold')
        self.ax2.text(0,-0.5, "Frame:\nCurrently Infected:\nHealthy People:\nImmune People:\nTotal Deaths:\nHealthcare Conditions:")
        self.ax2.text(0.54,-0.5, "Population:\nMasks Wearing:\nSocial Distancing:\nPeople Distancing:\nTotal Infected:\n")
        self.ax.text(0,1.06, "Simulation", fontsize='xx-large' , fontweight='bold')
        self.text = self.ax2.text(0.33, -0.5, "%i \n%i \n%s \n%s \n%s \n%s" %(0,len(infected_x),str(len(healthy_x)) + " or 0%", str(len(immune_x)) + " or 0%",str(len(dead_x)) + " or 0%",self.healthcare_status))
        self.text2 = self.ax2.text(0.81,-0.5,"%d \n%s \n%s \n%s \n%s\n" % (self.putil.size, self.mask_wearing_info, self.social_distancing_info, self.social_distancing_num , total_infected))

        return self.scat, self.scat2, self.scat3, self.scat4, self.currently_infected, self.total_infected, 

    def update(self, frame):
        """
        Similar to the setup function but this updates the simulation

        Parameters
        ----------
        :param frame: Represents the current frame.
        
        Returns
        -------
        :returns Variables that store plot objects
        """

        if(frame % 1 == 0):    

            # Calling method to move people, and check and infect them and perform
            # other functions.
            self.putil.move(frame)
            
            # Get all the healthy, immune, infected, and dead people seperately 
            healthy_x = self.putil.population.get_all_healthy()[:, index.x_axis]
            healthy_y = self.putil.population.get_all_healthy()[:, index.y_axis]
            infected_x = self.putil.population.get_all_infected()[:, index.x_axis]
            infected_y = self.putil.population.get_all_infected()[:, index.y_axis]
            immune_x = self.putil.population.get_all_recovered()[:, index.x_axis]
            immune_y = self.putil.population.get_all_recovered()[:, index.y_axis]
            dead_x = self.putil.population.get_all_dead()[:, index.x_axis]
            dead_y = self.putil.population.get_all_dead()[:, index.y_axis]
            total_infected = self.putil.size - len(healthy_x)
            total_hospitalized = len(self.putil.persons[self.putil.persons[:,index.hospitalized] == 3])
            currently_infected = len(infected_x)

            # Update healthcare status
            if currently_infected > self.putil.total_healthcare_capacity*3/2:
                self.healthcare_status   = "Extreme"
            elif currently_infected > self.putil.total_healthcare_capacity:
                self.healthcare_status   = "Worse"
            elif currently_infected > self.putil.total_healthcare_capacity*2/3:
                self.healthcare_status   = "Manageable"
            else:
                self.healthcare_status   = "Normal"

            # Update Graphs
            data1 = np.c_[healthy_x,healthy_y]
            data2 = np.c_[infected_x,infected_y]
            data3 = np.c_[immune_x,immune_y]
            data4 = np.c_[dead_x,dead_y]

            if frame == self.putil.enforce_mask_wearing_at:
                self.mask_wearing_info = "Active" 
            
            if frame == self.putil.enforce_social_distance_at:
                self.social_distancing_info = "Active"

            self.text.set_text("%i \n%i \n%s \n%s \n%s \n%s" % (frame,len(infected_x), str(len(healthy_x)) + " or " + str(round(len(healthy_x)*100/self.putil.size,1)) + "%",
                                str(len(immune_x)) + " or " + str(round(len(immune_x)*100/self.putil.size,1)) + "%", str(len(dead_x)) + " or " + str(round(len(dead_x)*100/self.putil.size,1)) + "%",
                                self.healthcare_status))
            self.text2.set_text("%s \n%s \n%s \n%s \n%s\n" % (self.putil.size, self.mask_wearing_info, self.social_distancing_info, self.social_distancing_num , total_infected))
            self.scat.set_offsets(data1)
            self.scat2.set_offsets(data2)
            self.scat3.set_offsets(data3)
            self.scat4.set_offsets(data4)
   
            self.infected.append(len(infected_x))
            self.infected_total.append(self.putil.size - len(healthy_x))
            self.deaths.append(len(dead_x))
            self.frames.append(frame)
            self.immunes.append(len(immune_x))

            self.currently_infected.set_ydata(self.infected)
            self.currently_infected.set_xdata(self.frames)

            self.total_deaths.set_ydata(self.deaths)
            self.total_deaths.set_xdata(self.frames)

            self.total_immune.set_ydata(self.immunes)
            self.total_immune.set_xdata(self.frames)

            
        
        return self.scat, self.scat2, self.scat3, self.scat4, self.currently_infected,


        

if __name__ == "__main__":
    v = Visualization()