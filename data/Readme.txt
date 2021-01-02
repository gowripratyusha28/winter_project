In every csv-file there are 10 different sequences (samples) for the same parameters, separated by "-99"

Artificial Data: 
Single sourced, hence a list of destinations is given.
"weibull0.6_1k-req_100hosts" means weibull shape parameter = 0.6, 1000 requests using 100 hosts
	in the folder: p0.01 means temporal locality p = 0.01 (probability of repeating the last request)

Real Data:
Source- and destination-IDs available.
"fb_clustA_1k_100hosts" means facebook-DB, collection clusterA, 1000 slice-size of the DB, 100 hosts
    # databases: 'facebook', 'microsoft', 'hpc', 'p_fab'
    #
    # facebook clusters:
    # clusterA, clusterB, clusterC
    #
    # microsoft clusters:
    # projector
    #
    # hpc clusters:
    # cesar_mocfe, cesar_nekbone, exact_boxlib_cns_nospec_large, exact_boxlib_multigrid_c_large
    #
    # p_fab clusters:
    # trace_0_1, trace_0_5, trace_0_8