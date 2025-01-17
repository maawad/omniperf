# Grafana-based Analysis

```eval_rst
.. toctree::
   :glob:
   :maxdepth: 4
```

## Features
The Omniperf Grafana GUI Analyzer supports the following features to facilitate MI GPU performance profiling and analysis:

- System and IP-Block Speed-of-Light (SOL)
- Multiple normalization options, including per-cycle, per-wave, per-kernel and per-second.
- Baseline comparisons 
- Regex based Dispatch ID filtering
- Roofline Analysis
- Detailed per IP Block performance counters and metrics
  - CPC/CPF
  - SPI
  - SQ
  - SQC
  - TA/TD
  - TCP
  - TCC (both aggregated and per-channel perf info)

### Speed-of-Light
Speed-of-light panels are provided at both the system and per IP block level to help diagnosis performance bottlenecks. The performance numbers of the workload under testing are compared to the theoretical maximum, (e.g. floating point operations, bandwidth, cache hit rate, etc.), to indicate the available room to further utilize the hardware capability.

### Multi Normalization

Multiple performance number normalizations are provided to allow performance inspection within both HW and SW context. The following normalizations are permitted:
- per cycle
- per wave
- per kernel
- per second

### Baseline Comparison
Omniperf enables baseline comparison to allow checking A/B effect. The current release limits the baseline comparison to the same SoC. Cross comparison between SoCs is in development.

For both the Current Workload and the Baseline Workload, one can independently setup the following filters to allow fine grained comparions:
- Workload Name 
- GPU ID filtering (multi selection)
- Kernel Name filtering (multi selection)
- Dispatch ID filtering (Regex filtering)
- Omniperf Panels (multi selection)

### Regex based Dispatch ID filtering
This release enables regex based dispatch ID filtering to flexibly choose the kernel invocations. One may refer to [Regex Numeric Range Generator](https://3widgets.com/), to generate typical number ranges. 

For example, if one wants to inspect Dispatch Range from 17 to 48, inclusive, the corresponding regex is : **(1[7-9]|[23]\d|4[0-8])**. The generated express can be copied over for filtering.

### Incremental Profiling
Omniperf supports incremental profiling to significantly speed up performance analysis.

> Refer to [*IP Block profiling*](https://amdresearch.github.io/omniperf/performance_analysis.html#ip-block-profiling) section for this command. 

By default, the entire application is profiled to collect perfmon counter for all IP blocks, giving a system level view of where the workload stands in terms of performance optimization opportunities and bottlenecks. 

After that one may focus on only a few IP blocks, (e.g., L1 Cache or LDS) to closely check the effect of software optimizations, without performing application replay for all other IP Blocks. This saves lots of compute time. In addition, the prior profiling results for other IP blocks are not overwritten. Instead, they can be merged during the import to piece together the system view. 

### Color Coding
The uniform color coding is applied to most visualizations (bars, table, diagrams etc). Typically, Yellow color means over 50%, while Red color mean over 90% percent, for easy inspection.

### Global Variables and Configurations

![Grafana GUI Global Variables](images/global_variables.png)

## Grafana GUI Import
The omniperf database `--import` option imports the raw profiling data to Grafana's backend MongoDB database. This step is only required for Grafana GUI based performance analysis. 

Default username and password for MongoDB (to be used in database mode) are as follows:

 - Username: **temp**
 - Password: **temp123**

Each workload is imported to a separate database with the following naming convention:

    omniperf_<team>_<database>_<soc>

e.g., omniperf_asw_vcopy_mi200.

Below is the sample command to import the *vcopy* profiling data.

```shell
$ omniperf database --help
ROC Profiler:  /usr/bin/rocprof

usage: 
                                        
omniperf database <interaction type> [connection options]

                                        

-------------------------------------------------------------------------------
                                        
Examples:
                                        
        omniperf database --import -H pavii1 -u temp -t asw -w workloads/vcopy/mi200/
                                        
        omniperf database --remove -H pavii1 -u temp -w omniperf_asw_sample_mi200
                                        
-------------------------------------------------------------------------------

                                        

Help:
  -h, --help             show this help message and exit

General Options:
  -v, --version          show program's version number and exit
  -V, --verbose          Increase output verbosity

Interaction Type:
  -i, --import                                          Import workload to Omniperf DB
  -r, --remove                                          Remove a workload from Omniperf DB

Connection Options:
  -H , --host                                           Name or IP address of the server host.
  -P , --port                                           TCP/IP Port. (DEFAULT: 27018)
  -u , --username                                       Username for authentication.
  -p , --password                                       The user's password. (will be requested later if it's not set)
  -t , --team                                           Specify Team prefix.
  -w , --workload                                       Specify name of workload (to remove) or path to workload (to import)
  -k , --kernelVerbose                                  Specify Kernel Name verbose level 1-5. 
                                                        Lower the level, shorter the kernel name. (DEFAULT: 2) (DISABLE: 5)
```

**omniperf import for vcopy:**
```shell
$ omniperf database --import -H pavii1 -u temp -t asw -w workloads/vcopy/mi200/
ROC Profiler:  /usr/bin/rocprof
 
--------
Import Profiling Results
--------
 
Pulling data from  /home/amd/xlu/test/workloads/vcopy/mi200
The directory exists
Found sysinfo file
KernelName shortening enabled
Kernel name verbose level: 2
Password:
Password recieved
-- Conversion & Upload in Progress --
  0%|                                                                                                                                                                                                             | 0/11 [00:00<?, ?it/s]/home/amd/xlu/test/workloads/vcopy/mi200/SQ_IFETCH_LEVEL.csv
  9%|█████████████████▉                                                                                                                                                                                   | 1/11 [00:00<00:01,  8.53it/s]/home/amd/xlu/test/workloads/vcopy/mi200/pmc_perf.csv
 18%|███████████████████████████████████▊                                                                                                                                                                 | 2/11 [00:00<00:01,  6.99it/s]/home/amd/xlu/test/workloads/vcopy/mi200/SQ_INST_LEVEL_SMEM.csv
 27%|█████████████████████████████████████████████████████▋                                                                                                                                               | 3/11 [00:00<00:01,  7.90it/s]/home/amd/xlu/test/workloads/vcopy/mi200/SQ_LEVEL_WAVES.csv
 36%|███████████████████████████████████████████████████████████████████████▋                                                                                                                             | 4/11 [00:00<00:00,  8.56it/s]/home/amd/xlu/test/workloads/vcopy/mi200/SQ_INST_LEVEL_LDS.csv
 45%|█████████████████████████████████████████████████████████████████████████████████████████▌                                                                                                           | 5/11 [00:00<00:00,  9.00it/s]/home/amd/xlu/test/workloads/vcopy/mi200/SQ_INST_LEVEL_VMEM.csv
 55%|███████████████████████████████████████████████████████████████████████████████████████████████████████████▍                                                                                         | 6/11 [00:00<00:00,  9.24it/s]/home/amd/xlu/test/workloads/vcopy/mi200/sysinfo.csv
 64%|█████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████▎                                                                       | 7/11 [00:00<00:00,  9.37it/s]/home/amd/xlu/test/workloads/vcopy/mi200/roofline.csv
 82%|█████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████▏                                   | 9/11 [00:00<00:00, 12.60it/s]/home/amd/xlu/test/workloads/vcopy/mi200/timestamps.csv
100%|████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 11/11 [00:00<00:00, 11.05it/s]
9 collections added.
Workload name uploaded
-- Complete! --
```

## Omniperf Panels

### Overview

There are currently 18 main panel categories available for analyzing the compute workload performance. Each category contains several panels for close inspection of the system performance.

- Kernel Statistics
  - Kernel time histogram
  - Top Ten bottleneck kernels
- System Speed-of-Light
  - Speed-of-Light
  - System Info table
- Memory Chart Analysis
- Roofline Analysis
  - FP32/FP64
  - FP16/INT8
- Command Processor
  - Command Processor - Fetch (CPF)
  - Command Processor - Controller (CPC)
- Shader Processing Input (SPI)
  - SPI Stats
  - SPI Resource Allocations
- Wavefront Launch
  - Wavefront Launch Stats
  - Wavefront runtime stats
  - per-SE Wavefront Scheduling performance
- Wavefront Lifetime
  - Wavefront lifetime breakdown
  - per-SE wavefront life (average)
  - per-SE wavefront life (histogram)
- Wavefront Occupancy
  - per-SE wavefront occupancy
  - per-CU wavefront occupancy
- Compute Unit - Instruction Mix
  - per-wave Instruction mix
  - per-wave VALU Arithmetic instruction mix
  - per-wave MFMA Arithmetic instruction mix
- Compute Unit - Compute Pipeline
  - Speed-of-Light: Compute Pipeline
  - Arithmetic OPs count
  - Compute pipeline stats
  - Memory latencies
- Local Data Share (LDS)
  - Speed-of-Light: LDS
  - LDS stats
- Instruction Cache
  - Speed-of-Light: Instruction Cache
  - Instruction Cache Accesses
- Constant Cache
  - Speed-of-Light: Constant Cache
  - Constant Cache Accesses
  - Constant Cache - L2 Interface stats
- Texture Address and Texture Data
  - Texture Address (TA)
  - Texture Data (TD)
- L1 Cache
  - Speed-of-Light: L1 Cache
  - L1 Cache Accesses
  - L1 Cache Stalls
  - L1 - L2 Transactions
  - L1 - UTCL1 Interface stats
- L2 Cache
  - Speed-of-Light: L2 Cache
  - L2 Cache Accesses
  - L2 - EA Transactions
  - L2 - EA Stalls
- L2 Cache Per Channel Performance
  - Per-channel L2 Hit rate
  - Per-channel L1-L2 Read requests
  - Per-channel L1-L2 Write Requests
  - Per-channel L1-L2 Atomic Requests
  - Per-channel L2-EA Read requests
  - Per-channel L2-EA Write requests
  - Per-channel L2-EA Atomic requests
  - Per-channel L2-EA Read latency
  - Per-channel L2-EA Write latency
  - Per-channel L2-EA Atomic  latency
  - Per-channel L2-EA Read stall (I/O, GMI, HBM)
  - Per-channel L2-EA Write stall (I/O, GMI, HBM, Starve)

Most panels are designed around a specific IP block to thoroughly understand its behavior. Additional panels, including custom panels, could also be added to aid the performance analysis.

### System Info Panel
![System Info Panel](images/System_info_panel.png)
### Kernel Statistics

#### Kernel Time Histogram
![Kernel Time Histogram](images/Kernel_time_histogram.png)
#### Top Bottleneck Kernels
![Top Bottleneck Kernels](images/Top_bottleneck_kernels.png)
#### Top Bottleneck Dispatches
![Top Bottleneck Dispatches](images/Top_bottleneck_dispatches.png)
#### Current and Baseline Dispatch IDs (Filtered)
![Current and Baseline Dispatch IDs](images/Current_and_baseline_dispatch_ids.png)

### System Speed-of-Light
![System Speed-of-Light](images/System_speed_of_light.png)

### Memory Chart Analysis
> Note: The Memory Chart Analysis support multiple normalizations. Due to the space limit, all transactions, when normalized to per-sec, default to unit of Billion transactions per second.

![Memory Chart Analysis](images/Memory_chart_analysis.png)

### Roofline Analysis
![Roofline Analysis](images/Roofline_analysis.png)
### Command Processor
![Command Processor](images/Command_processor.png)
### Shader Processing Input (SPI)
![Shader Processing Input](images/Shader_processing_input.png)
### Wavefront Launch
![Wavefront Launch](images/Wavefront_launch.png)

### Compute Unit - Instruction Mix
#### Instruction Mix
![Instruction Mix](images/Instruction_mix.png)
#### VALU Arithmetic Instruction Mix
![VALU Arithmetic Instruction Mix](images/VALU_arithmetic_instruction_mix.png)
#### MFMA Arithmetic Instruction Mix
![MFMA Arithmetic Instruction Mix](images/MFMA_arithmetic_instruction_mix.png)
#### VMEM Arithmetic Instruction Mix
![VMEM Arithmetic Instruction Mix](images/VMEM_arithmetic_intensity_mix.png)

### Compute Unit - Compute Pipeline
#### Speed-of-Light
![Speed-of-Light](images/Comp_pipe_sol.png)
#### Compute Pipeline Stats
![Compute Pipeline Stats](images/Compute_pipeline_stats.png)
#### Arithmetic Operations
![Arithmetic Operations](images/Arithmetic_operations.png)
#### Memory Latencies
![Memory Latencies](images/Memory_latencies.png)

### Local Data Share (LDS)
#### Speed-of-Light
![Speed-of-Light](images/LDS_sol.png)
#### LDS Stats
![LDS Stats](images/LDS_stats.png)

### Instruction Cache
#### Speed-of-Light
![Speed-of-Light](images/Instruc_cache_sol.png)
#### Instruction Cache Stats
![Instruction Cache Stats](images/Instruction_cache_stats.png)

### Scalar L1D Cache
#### Speed-of-Light
![](images/L1D_sol.png)
#### Constant Cache Stats
![Constant Cache Stats](images/Vec_L1D_cache_accesses.png)
#### Constant Cache - L2 Interface
![Constant Cache - L2 Interface](images/Constant_cache_l2_interface.png)

### Texture Address and Texture Data
#### Texture Address (TA)
![Texture Address](images/Texture_address.png)
#### Texture Data (TD)
![Texture Data](images/Texture_data.png)

### Vector L1D Cache
#### Speed-of-Light
![Speed-of-Light](images/Vec_L1D_cache_sol.png)
#### Vector L1D Cache Accesses
![Vector L1D Cache Accesses](images/Vec_L1D_cache_accesses.png)
#### L1 Cache Stalls
![L1 Cache Stalls](images/L1_cache_stalls.png)
#### L1 - L2 Transactions
![L1 - L2 Transactions](images/L1_l2_transactions.png)
#### L1 - UTCL1 Interface Stats
![L1 - UTCL1 Interface Stats](images/L1_utcl1_transactions.png)

### L2 Cache
#### Speed-of-Light
![Speed-of-Light](images/L2_cache_sol.png)
#### L2 Cache Accesses
![L2 Cache Accesses](images/L2_cache_accesses.png)
#### L2 - EA Transactions
![L2 - EA Transactions](images/L2_ea_transactions.png)
#### L2 - EA Stalls
![L2 - EA Stalls](images/L2_ea_stalls.png)

### L2 Cache Per Channel Performance
#### L1-L2 Transactions
![L1-L2 Transactions](images/L1_l2_transactions_per_channel.png)
#### L2-EA Transactions
![L2-EA Transactions](images/L2_ea_transactions_per_channel.png)
#### L2-EA Latencies
![L2-EA Latencies](images/L2_ea_latencies_per_channel.png)
#### L2-EA Stalls
![L2-EA Stalls](images/L2_ea_stalls_per_channel.png)
#### L2-EA Write Stalls
![L2-EA Write Stalls](images/L2_ea_write_stalls_per_channel.png)
#### L2-EA Write Starvation
![L2-EA Write Starvation](images/L2_ea_write_starvation_per_channel.png)