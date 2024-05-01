from __future__ import print_function
from game import sd_peers, sd_spots, sd_domain_num, init_domains, \
    restrict_domain, SD_DIM, SD_SIZE
import random, copy
class AI:
    def __init__(self):
        self.conflict = False

    def solve(self, problem):
        domains = init_domains()
        restrict_domain(domains, problem)

        # TODO: implement backtracking search.

        # TODO: delete this block ->
        # Note that the display and test functions in the main file take domains as inputs.
        #   So when returning the final solution, make sure to take your assignment function
        #   and turn the value into a single element list and return them as a domain map.
        #for spot in sd_spots:
        #    domains[spot] = [1]
        #return domains
        # <- TODO: delete this block
        assignment = {}
        decision_stack = []
        while True:
            assignment, domains = self.propagate(problem, assignment, domains)
            if not self.conflict:
                if self.all_assigned(assignment):
                    return self.solution(assignment)
                else:
                    assignment, unassigned_x = self.make_decision(problem,assignment, domains)
                    if unassigned_x == None:
                        return self.solution(assignment)
                    decision_stack.append((copy.deepcopy(assignment), unassigned_x, copy.deepcopy(domains)))
            else:
                if not decision_stack:
                    return None
                else:
                    self.conflict = False
                    assignment, domains = self.backtrack(decision_stack)

    # TODO: add any supporting function you need
    def all_assigned(self,assignment):
        for spot in sd_spots:
            if spot not in assignment:
                return False
        return True
    def make_decision(self,problem,assignment,domains):
        for x in sd_spots:
            if x not in assignment:
                val = domains[x][0] #first choice is always fastest instead of random for some reason
                assignment[x] = val
                return assignment, x
        return assignment, None


    def backtrack(self,decision_stack):
        assignment, unassigned_x, domains = decision_stack.pop()
        a = assignment[unassigned_x]
        domains[unassigned_x].remove(a)
        del assignment[unassigned_x]
        return assignment, domains

    def propagate(self,problem,assignment,domains):
        self.conflict = False

        while True:
            updated = False
            for xi in sd_spots:
                if len(domains[xi]) == 1 and xi not in assignment:
                    a = domains[xi][0]
                    assignment[xi] = a
                    updated = True

            for xi in sd_spots:
                if len(domains[xi]) > 1 and xi in assignment:
                    a = assignment[xi]
                    domains[xi] = [a]
                    updated = True

            for xi in sd_spots:
                if len(domains[xi]) == 0:
                    self.conflict = True
                    updated = True
                    return assignment, domains
            #i think good

            #this works as expected
            for xi in sd_spots:
                for xj in sd_peers[xi]:
                    if len(domains[xi]) ==1: #cell is filled
                        val = domains[xi][0]
                        if val in domains[xj] and len(domains[xj]) >0:
                            if len(domains[xj]) ==1: #THE BREAD AND BUTTER BABY 6 TESTS PASS NOW PASSES TO EVERY SINGLE ONE WHOOOOO BUDDY
                                self.conflict = True
                                return assignment,domains
                            domains[xj].remove(val)
                            updated = True
            return assignment,domains
            if updated:
                return assignment,domains
    def solution(self,assignment):
        domain_map = {}
        for spot in sd_spots:
            if spot in assignment:
                domain_map[spot] = [assignment[spot]]
        return domain_map
    #### The following templates are only useful for the EC part #####

    # EC: parses "problem" into a SAT problem
    # of input form to the program 'picoSAT';
    # returns a string usable as input to picoSAT
    # (do not write to file)

    def sat_encode(self, problem):
        text = ""

        # TODO: write CNF specifications to 'text'

        return text

    # EC: takes as input the dictionary mapping
    # from variables to T/F assignments solved for by picoSAT;
    # returns a domain dictionary of the same form
    # as returned by solve()
    def sat_decode(self, assignments):
        # TODO: decode 'assignments' into domains

        # TODO: delete this ->
        domains = {}
        for spot in sd_spots:
            domains[spot] = [1]
        return domains
        # <- TODO: delete this
