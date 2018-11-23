"""
.. module:: example_multisampling
  :synopsis: Example multisampling strategy
.. moduleauthor:: David Eriksson <dme65@cornell.edu>
"""

from pySOT.optimization_problems import Ackley
#from pySOT.adaptive_sampling import CandidateDYCORS, GeneticAlgorithm, MultiStartGradient, MultiSampling
from pySOT.strategy import SRBFStrategy
from pySOT.surrogate import RBFInterpolant, CubicKernel, LinearTail
from pySOT.experimental_design import SymmetricLatinHypercube
from poap.controller import SerialController
import numpy as np
import os.path
import logging


def example_multisampling():
    return


    if not os.path.exists("./logfiles"):
        os.makedirs("logfiles")
    if os.path.exists("./logfiles/example_multisampling.log"):
        os.remove("./logfiles/example_multisampling.log")
    logging.basicConfig(filename="./logfiles/example_multisampling.log",
                        level=logging.INFO)

    print("\nNumber of threads: 1")
    print("Maximum number of evaluations: 200")
    print("Sampling method: CandidateDYCORS, Genetic Algorithm, Multi-Start Gradient")
    print("Experimental design: Latin Hypercube")
    print("Surrogate: Cubic RBF")

    nthreads = 1
    maxeval = 200
    nsamples = nthreads

    data = Ackley(dim=10)
    print(data.info)

    # Create a strategy and a controller
    sampling_method = [CandidateDYCORS(data=data, numcand=100*data.dim),
                       GeneticAlgorithm(data=data), MultiStartGradient(data=data)]
    controller = SerialController(data.eval)
    controller.strategy = \
        SRBFStrategy(
            worker_id=0, opt_prob=data, maxeval=maxeval, batch_size=nsamples,
            surrogate=RBFInterpolant(data.dim, kernel=CubicKernel(), tail=LinearTail(data.dim), maxpts=maxeval),
            exp_design=SymmetricLatinHypercube(dim=data.dim, npts=2*(data.dim+1)),
            sampling_method=MultiSampling(sampling_method, [0, 1, 0, 2]))

    result = controller.run()
    best, xbest = result.value, result.params[0]

    print('Best value: {0}'.format(best))
    print('Best solution: {0}\n'.format(
        np.array_str(xbest, max_line_width=np.inf,
                     precision=5, suppress_small=True)))


if __name__ == '__main__':
    example_multisampling()