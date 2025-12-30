---
tags: [gpu, nvidia, diagnostics, hpc]
---
# GPU Diagnostics Analysis

Analyze GPU diagnostic output to identify hardware or configuration issues.

## Key Data Sources
- `nvidia-smi -q` output
- `nvidia-smi --query-gpu=...` metrics
- `dcgmi diag` results
- dmesg GPU-related messages
- `/var/log/nvidia-*` logs

## Critical Checks

### GPU Health
- [ ] All GPUs visible and accessible
- [ ] Clock speeds at expected levels (not throttled)
- [ ] Temperature within spec (<85C typical)
- [ ] Power draw consistent with workload
- [ ] No row remapping or memory errors

### NVLink/NVSwitch
- [ ] All NVLink lanes active
- [ ] No CRC or replay errors
- [ ] Fabric topology as expected

### PCIe
- [ ] Full link width (x16 for GPUs)
- [ ] Expected generation (Gen4/Gen5)
- [ ] No AER errors in dmesg

### Memory
- [ ] ECC enabled and no uncorrectable errors
- [ ] Memory utilization as expected
- [ ] No SRAM parity errors

## Fault Code Mapping
Provide specific fault codes for identified issues:
- GPU_CLOCK_THROTTLE
- GPU_MEMORY_ERROR
- NVLINK_INACTIVE
- PCIE_WIDTH_REDUCED
- THERMAL_LIMIT
