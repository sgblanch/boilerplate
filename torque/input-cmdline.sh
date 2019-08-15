#!/bin/bash

########################################################################
# Resource requests for the scheduler

#PBS -q copperhead
#PBS -l walltime=8:00:00
#PBS -l nodes=1:ppn=8
#PBS -l mem=127gb
#PBS -N bwa-mem
#PBS -j oe -o bwa-mem.log

# usage:
#   qsub -F "reference.fasta reads1.fastq reads2.fastq output.bam" input-variables.sh

########################################################################
# Configure bash, making it more programming friendly

IFS=$'\n'          # Internal field seperator is newline
set -eu            # Exit on error, undefined variable is error
set -o noclobber   # Prevent shell (bash) from overwriting files
shopt -s nullglob  # Failed glob (e.g. *.bam) returns empty string
umask 0007         # Files created will be writable by user's group


########################################################################
# Load needed modules and print loaded modules to log file

module load bwa samtools
module list


########################################################################
# Set up temporary files and directories and try to clean them up when
# finished

export TMPDIR="$(mktemp -dp "${TMPDIR:-/tmp}")"

# Any custom tmp files go here
TMP_SAM="$(mktemp -p "${TMPDIR}" bwa-mem.XXXXXXXX.sam)"

cleanup() {
    printf "cleaning up: '%s' '%s'\n" "${TMP_SAM}" "${TMPDIR}"
    rm    "${TMP_SAM}"
    rm -r "${TMPDIR}"
}
trap cleanup 1 2 30 15 20 ERR EXIT


########################################################################

# PBS_O_WORKDIR is directory where job was submitted (where you ran qsub)
cd "${PBS_O_WORKDIR}"


# Reference sequence (FASTA)
REFERENCE="$1"
# First read file (FASTA/Q)
READS_1="$2"
# Second read file (FASTA/Q)
READS_2="$3"
# Output file name (BAM)
OUT_BAM="$4"

# Run BWA, output the SAM to a temporary file
#
# Your Homework: Read up on bwa's -C and -R options
#   -R "Header" -- sets the SAM ReadGroup header.  Should always be set
#   -C -- appends FASTA/Q comment to SAM output.  Comment must already
#         conform to SAM spec.  Only set when this is true
bwa mem -t "${PBS_NUM_PPN:-1}" \
        "${REFERENCE}" "${READS_1}" "${READS_2}" > "${TMP_SAM}"
printf "%s: bwa mem finished\n" "$(date)"

# Sort the temporary SAM file and write it out the final BAM
samtools sort -@ "${PBS_NUM_PPN:-1}" -m 7G -o "${OUT_BAM}" "${TMP_SAM}"
printf "%s: samtools sort finished\n" "$(date)"

# Index the sorted BAM file
samtools index "${OUT_BAM}"