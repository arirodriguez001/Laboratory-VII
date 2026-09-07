#!/bin/bash
#
## En SBATCH los comentarios son: "## ...." 
#
#
#SBATCH -J PHITS_INTELMPI       # Job NAME (human input)
#SBATCH -p COMPARTIDA   # Job QUEUE (human) COMPARTIDA
#SBATCH -n 32                    # number of cpu cores (human input)
#SBATCH --nodes=1   # number of nodes
#SBATCH --wait-all-nodes=1       # Do not begin execution until all nodes are ready for use
#SBATCH -o %j.slurm.out          # STDOUT file
#SBATCH -e %j.slurm.err          # STDERR file
#SBATCH --mem-per-cpu=1G         # Minimum memory required per allocated CPU
#SBATCH --cpu-freq high          # Set the highest available cpu frequency
#SBATCH --verbose                # Be verbose
#SBATCH -J "sin_atenuador"      # job name
#SBATCH --mail-user=sebastian.gossio2010@gmail.com   # email address
#SBATCH --mail-type=END
#
#
#More options: https://slurm.schedmd.com/sbatch.html
## Ejemplo de comentario SBATCH.
##SBATCH  --hint=nomultithread   # TURN OFF hyperthreading
##SBATCH  --hint=multithread     # TURN ON  hyperthreading
##SBATCH  --threads-per-core=1   # Number of threads per core to allocate (use "1" with --hint=nomultithread)
#
############################## MAIN ################################


#Limpia enviroment
module purge

#Suma la posibilidad de cargar modulos propios del usuario
module load use.own 

#Modulo MKL y Compiladores intel
module load intel/intel_2015.3.187

#Modulo Intel MPI 5
module load intel/impi_5.0.3.048

#Modulo para usar solo infiniband
module load intel/impi_fabric_ib

#Modulo para cuando se usa hypertherading (mirar si estan seteadas las opciones --hint=[no]multithread)
module load intel/impi_pinning_HT

#Modulo para cuando se quiere verbose y stats de intel mpi
#module load intel/impi_verbose

#Show user limits
echo
echo "Plantilla DCAP (intelmpi) rev. 201812131110"
echo
echo "User limits:"
echo
ulimit -a
echo
#Show slurm var:
echo
echo "Slurm enviroment:"
echo
if [ -z "$SLURM_NPROCS" ] ; then
    if [ -z "$SLURM_NTASKS_PER_NODE" ] ; then
      SLURM_NTASKS_PER_NODE=1
    fi
    SLURM_NPROCS=$(( $SLURM_JOB_NUM_NODES * $SLURM_NTASKS_PER_NODE ))
fi
echo "SLURM_JOBID             = " $SLURM_JOBID
echo "SLURM_JOB_NAME          = " $SLURM_JOB_NAME
echo "SLURM_JOB_NODELIST      = " $SLURM_JOB_NODELIST
echo "SLURM_JOB_PARTITION     = " $SLURM_JOB_PARTITION
echo "SLURM_JOB_ACCOUNT       = " $SLURM_JOB_ACCOUNT
echo "SLURM_MEM_PER_CPU       = " $SLURM_MEM_PER_CPU
echo "SLURM_MEM_PER_NODE      = " $SLURM_MEM_PER_NODE
echo "SLURM_ARRAY_JOB_ID      = " $SLURM_ARRAY_JOB_ID
echo "SLURM_ARRAY_TASK_ID     = " $SLURM_ARRAY_TASK_ID
echo "SLURMTMPDIR             = " $SLURMTMPDIR
echo "SLURM_RESTART_COUNT     = " $SLURM_RESTART_COUNT
echo "SLURM_TASKS_PER_NODE    = " $SLURM_TASKS_PER_NODE
echo "SLURM_NTASKS            = " $SLURM_NTASKS
echo "SLURM_NTASKS_PER_CORE   = " $SLURM_NTASKS_PER_CORE
echo "SLURM_NTASKS_PER_NODE   = " $SLURM_NTASKS_PER_NODE
echo "SLURM_NTASKS_PER_SOCKET = " $SLURM_NTASKS_PER_SOCKET
echo "SLURM_JOB_NUM_NODES     = " $SLURM_JOB_NUM_NODES 
echo "SLURM_NNODES            = " $SLURM_NNODES 
echo "SLURM_CPUS_PER_TASK     = " $SLURM_CPUS_PER_TASK
echo "SLURM_NPROCS            = " $SLURM_NPROCS
echo "SLURM_SUBMIT_DIR        = " $SLURM_SUBMIT_DIR
echo "SLURM_SUBMIT_HOST       = " $SLURM_SUBMIT_HOST
echo "SLURM_CPU_FREQ_REQ      = " $SLURM_CPU_FREQ_REQ

####Backward compatibility""""""
cd $SLURM_SUBMIT_DIR
srun --nodes=${SLURM_NNODES} bash -c 'hostname'> $SLURM_JOBID.machines
srun --nodes=${SLURM_NNODES} bash -c 'hostname' | sort -r | uniq > $SLURM_JOBID.mpd.hosts
NUM_PROCS=`cat $SLURM_JOBID.machines|wc -l`
NUM_NODES=`cat $SLURM_JOBID.mpd.hosts|wc -l`
echo NUM_PROCS = $NUM_PROCS
echo NUM_NODES = $NUM_NODES

#Launch
bin="/share/gidans/sebastiangossio/Programas/PIHTS-IFORT/phits/phits_LinIfort_MPI"
param="phits.in"
mpioption=""
echo
echo
echo -n "pwd: "
pwd
echo -np "which mpiexec: "
which mpiexec
echo -n "LD_LIBRARY_PATH: "
echo $LD_LIBRARY_PATH
echo -n "BEGIN MPI RUN started date-time: "
date --iso-8601=seconds
echo
echo
#Intel
export I_MPI_PMI_LIBRARY=/usr/lib64/libpmi.so
echo srun --verbose -n $SLURM_NTASKS $bin
srun --verbose -n $SLURM_NTASKS $bin
echo
echo
echo -n "END MPI RUN ended date-time: "
date --iso-8601=seconds
