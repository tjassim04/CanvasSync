"""
CanvasSync by Mathias Perslev
February 2017

--------------------------------------------

synchronizer.py, CanvasEntity class

The Synchronizer class is the highest level CanvasEntity object in the folder hierarchy.
It inherits from the CanvasEntity base class and extends its functionality to allow downloading
information on courses listed in the Canvas system.
A Course object is initialized for each course found and appended to a list of children under the Synchronizer object.
Synchronization, walking and printing of the folder hierarchy starts by invoking the method on the Synchronizer object
which in turn propagates the signal to all children objects.

The Synchronizer encapsulates a list of children Course objects.

"""

# Future imports
from __future__ import print_function

# Third party
from six import text_type

# CanvasSync modules
from CanvasSync.entities.course import Course
from CanvasSync.entities.canvas_entity import CanvasEntity
from CanvasSync.utilities import helpers
from CanvasSync.utilities.ANSI import ANSI
import threading
from queue import Queue

class Synchronizer(CanvasEntity):
    def __init__(self, settings, api, threads=None):
        """
        Constructor method, initializes base CanvasEntity class and adds all children
        Course objects to the list of children

        settings : object | A Settings object, has top-level sync path attribute
        api      : object | An InstructureApi object
        """

        if not settings.is_loaded():
            settings.load_settings("")
        self.threads = settings.threads or threads

        # Start sync by clearing the console window
        helpers.clear_console()

        # Get the corrected top-level sync path
        sync_path = helpers.get_corrected_path(settings.sync_path,
                                               parent_path=False, folder=True)

        # A dictionary to store lists of CanvasEntity objects
        # added to the hierarchy under a course ID number
        self.entities = {}

        # Initialize base class
        CanvasEntity.__init__(self,
                              id_number=-1,
                              name=u"",
                              sync_path=sync_path,
                              api=api,
                              settings=settings,
                              synchronizer=self,
                              identifier=u"synchronizer")

    def __repr__(self):
        """ String representation, overwriting base class method """
        return u"\n[*] Synchronizing to folder: %s\n" % self.sync_path

    def get_entities(self, course_id):
        """ Getter method for the list of Entities """
        return self.entities[course_id]

    def add_entity(self, entity, course_id):
        """ Add method to append CanvasEntity objects to the list of entities """
        self.entities[course_id].append(entity)

    def download_courses(self):
        """ Returns a dictionary of courses from the Canvas server """
        courses = self.api.get_courses()
        # Return all accessible courses
        return [course for course in courses if not course.get('access_restricted_by_date')]

    def add_courses(self):
        """
        Method that adds all Course objects representing Canvas courses to the
        list of children
        """
        # Download list of dictionaries representing Canvas crouses and
        # add them all to the list of children
        for course_information in self.download_courses():
            if "course_code" not in course_information:
                continue

            # Add an empty list to the entities dictionary that will
            # store entities when added
            self.entities[course_information[u"id"]] = []

            # Create Course object
            course = Course(course_information,
                            parent=self,
                            settings=self.settings)
            self.add_child(course)

    def walk(self):
        """ Walk by adding all Courses to the list of children """

        # Print initial walk message
        print(self)
        print(ANSI.format(u"\n[*] Mapping out the Canvas folder hierarchy. "
                          u"Please wait...", u"red"))
        self.add_courses()

        counter = [2]
        for course in self:
            course.walk(counter)

        return counter

    def sync(self):
        """
        1) Adding all Courses objects to the list of children
        2) Synchronize all children objects
        """
        print(text_type(self))

        self.add_courses()
        
        #Init a thread queue and enumerate and add all jobs for children
        course_queue = Queue()
        for course in self:
            course_queue.put(course)

        # Create and start threads
        num_threads = min(len(self.children), self.threads)
        threads = []
        for _ in range(num_threads):
            thread = threading.Thread(target=self._sync_course_worker, args=(course_queue,))
            thread.start()
            threads.append(thread)

        # Wait for all threads to complete
        for thread in threads:
            thread.join()

    def _sync_course_worker(self, course_queue):
        """
        Very Basic async handler. Gets the job done (no mismatched threads) but is not at all optimized.
        """
        while not course_queue.empty():
            try:
                course = course_queue.get(block=False)
                course.sync()
            except Queue.Empty:
                break
            finally:
                course_queue.task_done()

    def show(self):
        """ Show the folder hierarchy by printing every level """

        helpers.clear_console()
        print(u"\n")
        print(text_type(self))

        for course in self:
            course.show()
