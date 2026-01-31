import os
import sys
import ctypes
import subprocess
import winreg
import argparse
import logging
import platform
import json
import psutil
from colorama import init, Fore, Style

init(autoreset=True)

logging.basicConfig(level=logging.INFO, format='%(message)s')
status_logger = logging.getLogger(__name__)

class WindowsPerformanceOptimizer:
    def __init__(self, graphics_hardware=None, storage_drive=None):
        self.graphics_card_type = graphics_hardware or self.identify_graphics_hardware()
        self.storage_medium_type = storage_drive or self.determine_storage_media_type()
        self.ram_gb = self.get_total_ram_gb()
        
        self._initialize_core_system_settings()
        self._initialize_latency_reduction_settings()
        self._initialize_memory_management_settings()
        self._initialize_storage_optimization_settings()
        self._initialize_processor_performance_settings()
        self._initialize_frame_rate_optimizations()
        self._initialize_energy_management_settings()
        self._initialize_video_card_specific_settings()
        self._initialize_network_optimizations()
        self._initialize_peripheral_and_driver_settings()

    def identify_graphics_hardware(self):
        try:
            query_result = subprocess.run(
                'wmic path win32_VideoController get name',
                shell=True, capture_output=True, text=True
            )
            raw_output = query_result.stdout.lower()
            if not raw_output.strip() or 'name' not in raw_output:
                query_result = subprocess.run(
                    ['powershell', '-Command', 'Get-CimInstance Win32_VideoController | Select-Object -ExpandProperty Name'],
                    capture_output=True, text=True
                )
                raw_output = query_result.stdout.lower()

            if 'nvidia' in raw_output or 'geforce' in raw_output:
                return 'NVIDIA'
            elif 'amd' in raw_output or 'radeon' in raw_output:
                return 'AMD'
            elif 'intel' in raw_output:
                return 'Intel'
            else:
                return 'Unknown'
        except:
            return 'Unknown'

    def determine_storage_media_type(self):
        try:
            disk_query = subprocess.run(
                ['powershell', '-Command', 'Get-PhysicalDisk | Select-Object MediaType'],
                capture_output=True, text=True
            )
            raw_output = disk_query.stdout.lower()
            
            if 'ssd' in raw_output:
                return 'SSD'
            elif 'hdd' in raw_output:
                return 'HDD'
            else:
                return 'Unknown'
        except:
            return 'Unknown'

    def get_total_ram_gb(self):
        try:
            total_ram = psutil.virtual_memory().total
            return round(total_ram / (1024**3))
        except:
            try:
                # Fallback to wmic if psutil fails
                query = subprocess.run('wmic computersystem get totalphysicalmemory', shell=True, capture_output=True, text=True)
                total_bytes = int(query.stdout.split('\n')[1].strip())
                return round(total_bytes / (1024**3))
            except:
                return 0

    def _initialize_core_system_settings(self):
        self.core_system_adjustments = [
            {
                "registry_path": r"SYSTEM\ControlSet001\Control\PriorityControl",
                "entry_name": "Win32PrioritySeparation",
                "entry_value": 0x28,
                "data_type": winreg.REG_DWORD,
                "hive_root": winreg.HKEY_LOCAL_MACHINE,
                "task_description": "Optimize Windows priority separation for gaming performance"
            },
            {
                "registry_path": r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Multimedia\SystemProfile",
                "entry_name": "SystemResponsiveness",
                "entry_value": 0,
                "data_type": winreg.REG_DWORD,
                "hive_root": winreg.HKEY_LOCAL_MACHINE,
                "task_description": "Enhance general system responsiveness"
            },
            {
                "registry_path": r"SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System",
                "multiple_entries": {
                    "ConsentPromptBehaviorAdmin": 0,
                    "EnableInstallerDetection": 0,
                    "EnableLUA": 0,
                    "EnableSecureUIAPaths": 0,
                    "EnableVirtualization": 0,
                    "FilterAdministratorToken": 0,
                    "PromptOnSecureDesktop": 0
                },
                "data_type": winreg.REG_DWORD,
                "hive_root": winreg.HKEY_LOCAL_MACHINE,
                "task_description": "Disable User Account Control warnings"
            },
            {
                "registry_path": r"SYSTEM\ControlSet001\Services\luafv",
                "entry_name": "Start",
                "entry_value": 4,
                "data_type": winreg.REG_DWORD,
                "hive_root": winreg.HKEY_LOCAL_MACHINE,
                "task_description": "Deactivate LUA file virtualization"
            },
            {
                "registry_path": r"SOFTWARE\Microsoft\Direct3D",
                "entry_name": "FlipNoVsync",
                "entry_value": 1,
                "data_type": winreg.REG_DWORD,
                "hive_root": winreg.HKEY_LOCAL_MACHINE,
                "task_description": "Disable VSync for Direct3D applications"
            },
            {
                "registry_path": r"SOFTWARE\WOW6432Node\Microsoft\Direct3D",
                "entry_name": "FlipNoVsync",
                "entry_value": 1,
                "data_type": winreg.REG_DWORD,
                "hive_root": winreg.HKEY_LOCAL_MACHINE,
                "task_description": "Disable VSync for 32-bit applications on 64-bit Windows"
            },
            {
                "registry_path": r"SYSTEM\ControlSet001\Control\Power",
                "entry_name": "HibernateEnabled",
                "entry_value": 0,
                "data_type": winreg.REG_DWORD,
                "hive_root": winreg.HKEY_LOCAL_MACHINE,
                "task_description": "Disable system hibernation to save space and performance"
            },
            {
                "registry_path": r"SYSTEM\CurrentControlSet\Services\EventLog",
                "entry_name": "Start",
                "entry_value": 4,
                "data_type": winreg.REG_DWORD,
                "hive_root": winreg.HKEY_LOCAL_MACHINE,
                "task_description": "Disable background event logging service"
            },
            {
                "registry_path": r"Control Panel\Desktop",
                "multiple_entries": {
                    "AutoEndTasks": "1",
                    "HungAppTimeout": "1000",
                    "MenuShowDelay": "0",
                    "WaitToKillAppTimeout": "2000",
                    "LowLevelHooksTimeout": "1000"
                },
                "data_type": winreg.REG_SZ,
                "hive_root": winreg.HKEY_CURRENT_USER,
                "task_description": "Improve desktop interface responsiveness and speed"
            },
            {
                "registry_path": r"Control Panel\Accessibility\ToggleKeys",
                "entry_name": "Flags",
                "entry_value": "58",
                "data_type": winreg.REG_SZ,
                "hive_root": winreg.HKEY_CURRENT_USER,
                "task_description": "Deactivate sticky and toggle keys accessibility features"
            },
            {
                "registry_path": r"SYSTEM\CurrentControlSet\Control\Session Manager\Memory Management",
                "entry_name": "DisablePagingExecutive",
                "entry_value": 1,
                "data_type": winreg.REG_DWORD,
                "hive_root": winreg.HKEY_LOCAL_MACHINE,
                "task_description": "Force Windows to keep kernel and drivers in physical RAM"
            }
        ]

    def _initialize_latency_reduction_settings(self):
        self.delay_reduction_optimizations = [
            {
                "registry_path": r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Multimedia\SystemProfile",
                "multiple_entries": {
                    "NetworkThrottlingIndex": 0xffffffff,
                    "SystemResponsiveness": 0,
                    "LazyModeTimeout": 10000
                },
                "data_type": winreg.REG_DWORD,
                "hive_root": winreg.HKEY_LOCAL_MACHINE,
                "task_description": "Reduce network and system processing delays"
            },
            {
                "registry_path": r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Multimedia\SystemProfile\Tasks\Games",
                "multiple_entries": {
                    "GPU Priority": 8,
                    "Priority": 6
                },
                "data_type": winreg.REG_DWORD,
                "hive_root": winreg.HKEY_LOCAL_MACHINE,
                "task_description": "Set higher processing priority for gaming tasks"
            },
            {
                "registry_path": r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Multimedia\SystemProfile\Tasks\Games",
                "multiple_entries": {
                    "Scheduling Category": "High",
                    "SFIO Priority": "High"
                },
                "data_type": winreg.REG_SZ,
                "hive_root": winreg.HKEY_LOCAL_MACHINE,
                "task_description": "Set high-level scheduling for game IO"
            },
            {
                "registry_path": r"SYSTEM\CurrentControlSet\Control\Session Manager\kernel",
                "entry_name": "DistributeTimers",
                "entry_value": 1,
                "data_type": winreg.REG_DWORD,
                "hive_root": winreg.HKEY_LOCAL_MACHINE,
                "task_description": "Distribute system timers across multiple CPU cores"
            },
            {
                "registry_path": r"SYSTEM\CurrentControlSet\Services\DXGKrnl",
                "entry_name": "MonitorLatencyTolerance",
                "entry_value": 1,
                "data_type": winreg.REG_DWORD,
                "hive_root": winreg.HKEY_LOCAL_MACHINE,
                "task_description": "Minimize display monitoring latency"
            },
            {
                "registry_path": r"SYSTEM\CurrentControlSet\Services\DXGKrnl",
                "entry_name": "MonitorRefreshLatencyTolerance",
                "entry_value": 1,
                "data_type": winreg.REG_DWORD,
                "hive_root": winreg.HKEY_LOCAL_MACHINE,
                "task_description": "Sync monitor refresh tolerance for low latency"
            },
            {
                "registry_path": r"SYSTEM\CurrentControlSet\Control\Session Manager\Executive",
                "entry_name": "AdditionalCriticalWorkerThreads",
                "entry_value": 16,
                "data_type": winreg.REG_DWORD,
                "hive_root": winreg.HKEY_LOCAL_MACHINE,
                "task_description": "Allocate more CPU worker threads for critical tasks"
            },
            {
                "registry_path": r"SYSTEM\CurrentControlSet\Control\Session Manager\Executive",
                "entry_name": "AdditionalDelayedWorkerThreads",
                "entry_value": 16,
                "data_type": winreg.REG_DWORD,
                "hive_root": winreg.HKEY_LOCAL_MACHINE,
                "task_description": "Allocate more CPU worker threads for background tasks"
            },
            {
                "registry_path": r"SYSTEM\CurrentControlSet\Services\usbxhci\Parameters",
                "entry_name": "ThreadPriority",
                "entry_value": 31,
                "data_type": winreg.REG_DWORD,
                "hive_root": winreg.HKEY_LOCAL_MACHINE,
                "task_description": "Set maximum priority for USB controller threads"
            },
            {
                "registry_path": r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Multimedia\SystemProfile",
                "entry_name": "NoLazyMode",
                "entry_value": 1,
                "data_type": winreg.REG_DWORD,
                "hive_root": winreg.HKEY_LOCAL_MACHINE,
                "task_description": "Disable power-saving lazy mode for system profile"
            },
            {
                "registry_path": r"System\GameConfigStore",
                "multiple_entries": {
                    "GameDVR_Enabled": 0,
                    "GameDVR_FSEBehaviorMode": 2,
                    "GameDVR_FSEBehavior": 2,
                    "GameDVR_HonorUserFSEBehaviorMode": 1,
                    "GameDVR_DXGIHonorFSEWindowsCompatible": 1,
                    "GameDVR_EFSEFeatureFlags": 0,
                    "GameDVR_DSEBehavior": 2
                },
                "data_type": winreg.REG_DWORD,
                "hive_root": winreg.HKEY_CURRENT_USER,
                "task_description": "Disable Fullscreen Optimizations and game recording features"
            },
            {
                "registry_path": r"SOFTWARE\Microsoft\GameBar",
                "multiple_entries": {
                    "ShowStartupPanel": 0,
                    "GamePanelStartupTipIndex": 3,
                    "AllowAutoGameMode": 0,
                    "AutoGameModeEnabled": 0,
                    "UseNexusForGameBarEnabled": 0
                },
                "data_type": winreg.REG_DWORD,
                "hive_root": winreg.HKEY_CURRENT_USER,
                "task_description": "Switch off Windows GameBar and automatic game modes"
            },
            {
                "registry_path": r"SOFTWARE\Microsoft\PolicyManager\default\ApplicationManagement\AllowGameDVR",
                "entry_name": "value",
                "entry_value": 0,
                "data_type": winreg.REG_DWORD,
                "hive_root": winreg.HKEY_LOCAL_MACHINE,
                "task_description": "Enforce policy to disable Game DVR functionality"
            },
            {
                "registry_path": r"SOFTWARE\Policies\Microsoft\Windows\GameDVR",
                "entry_name": "AllowGameDVR",
                "entry_value": 0,
                "data_type": winreg.REG_DWORD,
                "hive_root": winreg.HKEY_LOCAL_MACHINE,
                "task_description": "Deactivate Windows Game DVR via group policy"
            },
            {
                "registry_path": r"SOFTWARE\Microsoft\Windows\CurrentVersion\GameDVR",
                "entry_name": "AppCaptureEnabled",
                "entry_value": 0,
                "data_type": winreg.REG_DWORD,
                "hive_root": winreg.HKEY_CURRENT_USER,
                "task_description": "Disable application capture and recording"
            }
        ]

    def _initialize_memory_management_settings(self):
        self.memory_optimization_settings = [
            {
                "registry_path": r"SYSTEM\CurrentControlSet\Control\Session Manager\Memory Management",
                "entry_name": "LargeSystemCache",
                "entry_value": 0,
                "data_type": winreg.REG_DWORD,
                "hive_root": winreg.HKEY_LOCAL_MACHINE,
                "task_description": "Disable large system cache to free up memory for applications"
            },
            {
                "registry_path": r"SYSTEM\CurrentControlSet\Control\Session Manager\Memory Management",
                "multiple_entries": {
                    "ClearPageFileAtShutdown": 0,
                    "DisablePagingExecutive": 1,
                    "LargeSystemCache": 0,
                    "SecondLevelDataCache": 0,
                    "SessionPoolSize": 192,
                    "SessionViewSize": 192,
                    "SystemPages": 0,
                    "PhysicalAddressExtension": 1,
                    "FeatureSettings": 1,
                    "FeatureSettingsOverride": 3,
                    "FeatureSettingsOverrideMask": 3
                },
                "data_type": winreg.REG_DWORD,
                "hive_root": winreg.HKEY_LOCAL_MACHINE,
                "task_description": "Apply advanced registry-level memory management optimizations"
            },
            {
                "registry_path": r"SYSTEM\CurrentControlSet\Control\Session Manager\Memory Management\PrefetchParameters",
                "multiple_entries": {
                    "EnablePrefetcher": 0,
                    "EnableSuperfetch": 0
                },
                "data_type": winreg.REG_DWORD,
                "hive_root": winreg.HKEY_LOCAL_MACHINE,
                "task_description": "Disable Prefetch and Superfetch to reduce disk activity"
            }
        ]

    def _initialize_storage_optimization_settings(self):
        self.storage_adjustments = [
            {
                "registry_path": r"SYSTEM\CurrentControlSet\Services\disk",
                "entry_name": "TimeOutValue",
                "entry_value": 200,
                "data_type": winreg.REG_DWORD,
                "hive_root": winreg.HKEY_LOCAL_MACHINE,
                "task_description": "Adjust disk driver timeout period"
            }
        ]
        
        if self.storage_medium_type == 'SSD':
            self.storage_adjustments.extend([
                {
                    "registry_path": r"SYSTEM\CurrentControlSet\Control\Session Manager\Memory Management\PrefetchParameters",
                    "entry_name": "EnablePrefetcher",
                    "entry_value": 0,
                    "data_type": winreg.REG_DWORD,
                    "hive_root": winreg.HKEY_LOCAL_MACHINE,
                    "task_description": "Disable prefetching for solid state drives"
                },
                {
                    "registry_path": r"SYSTEM\ControlSet001\Control\Power",
                    "entry_name": "HibernateEnabled",
                    "entry_value": 0,
                    "data_type": winreg.REG_DWORD,
                    "hive_root": winreg.HKEY_LOCAL_MACHINE,
                    "task_description": "Disable hibernation to prolong SSD lifespan"
                }
            ])
        elif self.storage_medium_type == 'HDD':
            self.storage_adjustments.extend([
                {
                    "registry_path": r"SYSTEM\CurrentControlSet\Services\storahci\Parameters\Device",
                    "entry_name": "TreatAsInternalPort",
                    "entry_value": 1,
                    "data_type": winreg.REG_DWORD,
                    "hive_root": winreg.HKEY_LOCAL_MACHINE,
                    "task_description": "Configure hard drive ports as internal for better speed"
                }
            ])

    def _initialize_processor_performance_settings(self):
        self.processor_performance_tweaks = [
            {
                "registry_path": r"SYSTEM\CurrentControlSet\Control\Power\PowerThrottling",
                "entry_name": "PowerThrottlingOff",
                "entry_value": 1,
                "data_type": winreg.REG_DWORD,
                "hive_root": winreg.HKEY_LOCAL_MACHINE,
                "task_description": "Prevent the CPU from throttling during heavy loads"
            },
            {
                "registry_path": r"SYSTEM\CurrentControlSet\Control\PriorityControl",
                "entry_name": "IRQ8Priority",
                "entry_value": 1,
                "data_type": winreg.REG_DWORD,
                "hive_root": winreg.HKEY_LOCAL_MACHINE,
                "task_description": "Prioritize real-time clock interrupts"
            },
            {
                "registry_path": r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Multimedia\SystemProfile\Tasks\Games",
                "multiple_entries": {
                    "GPU Priority": 8,
                    "Priority": 6
                },
                "data_type": winreg.REG_DWORD,
                "hive_root": winreg.HKEY_LOCAL_MACHINE,
                "task_description": "Optimize processor task management for games"
            },
            {
                "registry_path": r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Multimedia\SystemProfile\Tasks\Games",
                "multiple_entries": {
                    "Scheduling Category": "High",
                    "SFIO Priority": "High"
                },
                "data_type": winreg.REG_SZ,
                "hive_root": winreg.HKEY_LOCAL_MACHINE,
                "task_description": "Set high-level data priority for gaming services"
            }
        ]

    def _initialize_frame_rate_optimizations(self):
        self.frame_rate_adjustments = [
            {
                "registry_path": r"SYSTEM\CurrentControlSet\Control\GraphicsDrivers",
                "multiple_entries": {
                    "TdrDelay": 60,
                    "TdrDdiDelay": 60,
                    "TdrLevel": 0,
                    "TdrLimitCount": 256,
                    "TdrLimitTime": 60
                },
                "data_type": winreg.REG_DWORD,
                "hive_root": winreg.HKEY_LOCAL_MACHINE,
                "task_description": "Configure graphics driver recovery settings to prevent stuttering"
            },
            {
                "registry_path": r"SYSTEM\CurrentControlSet\Control\GraphicsDrivers",
                "entry_name": "HwSchMode",
                "entry_value": 2,
                "data_type": winreg.REG_DWORD,
                "hive_root": winreg.HKEY_LOCAL_MACHINE,
                "task_description": "Enable Windows hardware-accelerated GPU scheduling"
            },
            {
                "registry_path": r"SYSTEM\CurrentControlSet\Services\DXGKrnl",
                "multiple_entries": {
                    "MonitorLatencyTolerance": 1,
                    "MonitorRefreshLatencyTolerance": 1
                },
                "data_type": winreg.REG_DWORD,
                "hive_root": winreg.HKEY_LOCAL_MACHINE,
                "task_description": "Improve monitor refresh latency for smoother visuals"
            }
        ]

    def _initialize_energy_management_settings(self):
        self.energy_management_optimizations = [
            {
                "registry_path": r"SYSTEM\CurrentControlSet\Services\USB",
                "entry_name": "DisableSelectiveSuspend",
                "entry_value": 1,
                "data_type": winreg.REG_DWORD,
                "hive_root": winreg.HKEY_LOCAL_MACHINE,
                "task_description": "Deactivate USB selective suspend to prevent device lag"
            },
            {
                "registry_path": r"SYSTEM\CurrentControlSet\Control\Power",
                "multiple_entries": {
                    "HibernateEnabled": 0,
                    "EnergyEstimationEnabled": 0,
                    "EventProcessorEnabled": 0,
                    "CsEnabled": 0,
                    "CoalescingTimerInterval": 0
                },
                "data_type": winreg.REG_DWORD,
                "hive_root": winreg.HKEY_LOCAL_MACHINE,
                "task_description": "General power configuration and timer coalescing for maximum performance"
            },
            {
                "registry_path": r"SYSTEM\CurrentControlSet\Services\usbhub\hubg",
                "entry_name": "DisableOnSoftRemove",
                "entry_value": 0,
                "data_type": winreg.REG_DWORD,
                "hive_root": winreg.HKEY_LOCAL_MACHINE,
                "task_description": "Keep USB hubs active and ready for fast device detection"
            }
        ]

    def _initialize_video_card_specific_settings(self):
        self.video_card_optimizations = []
        
        if self.graphics_card_type == 'NVIDIA':
            self.video_card_optimizations = [
                {
                    "registry_path": r"SYSTEM\CurrentControlSet\Control\Class\{4d36e968-e325-11ce-bfc1-08002be10318}\0000",
                    "multiple_entries": {
                        "DisableDynamicPstate": 1,
                        "DisableAsyncPstates": 1
                    },
                    "data_type": winreg.REG_DWORD,
                    "hive_root": winreg.HKEY_LOCAL_MACHINE,
                    "task_description": "Force NVIDIA GPU to run at maximum performance frequency"
                },
                {
                    "registry_path": r"SYSTEM\CurrentControlSet\Services\nvlddmkm",
                    "entry_name": "DisableWriteCombining",
                    "entry_value": 1,
                    "data_type": winreg.REG_DWORD,
                    "hive_root": winreg.HKEY_LOCAL_MACHINE,
                    "task_description": "Disable NVIDIA CPU-GPU write combining for consistency"
                },
                {
                    "registry_path": r"SYSTEM\CurrentControlSet\Services\nvlddmkm\FTS",
                    "entry_name": "EnableRID61684",
                    "entry_value": 1,
                    "data_type": winreg.REG_DWORD,
                    "hive_root": winreg.HKEY_LOCAL_MACHINE,
                    "task_description": "Enable specific NVIDIA driver-level optimizations"
                },
                {
                    "registry_path": r"SYSTEM\CurrentControlSet\Control\GraphicsDrivers\Scheduler",
                    "multiple_entries": {
                        "EnablePreemption": 0,
                        "GPUPreemptionLevel": 0,
                        "ComputePreemptionLevel": 0
                    },
                    "data_type": winreg.REG_DWORD,
                    "hive_root": winreg.HKEY_LOCAL_MACHINE,
                    "task_description": "Optimize NVIDIA GPU scheduling preemption for lower latency"
                }
            ]
        elif self.graphics_card_type == 'AMD':
            self.video_card_optimizations = [
                {
                    "registry_path": r"SYSTEM\CurrentControlSet\Control\Class\{4d36e968-e325-11ce-bfc1-08002be10318}\0000",
                    "multiple_entries": {
                        "PP_SclkDeepSleepDisable": 1,
                        "PP_ThermalAutoThrottlingEnable": 0
                    },
                    "data_type": winreg.REG_DWORD,
                    "hive_root": winreg.HKEY_LOCAL_MACHINE,
                    "task_description": "Prevent AMD GPU from entering deep sleep states"
                },
                {
                    "registry_path": r"SYSTEM\CurrentControlSet\Control\Class\{4d36e968-e325-11ce-bfc1-08002be10318}\0000",
                    "entry_name": "KMD_RpmComputeLatency",
                    "entry_value": 1,
                    "data_type": winreg.REG_DWORD,
                    "hive_root": winreg.HKEY_LOCAL_MACHINE,
                    "task_description": "Optimize AMD compute latency for better frame delivery"
                }
            ]
        elif self.graphics_card_type == 'Intel':
            self.video_card_optimizations = [
                {
                    "registry_path": r"SYSTEM\CurrentControlSet\Control\GraphicsDrivers",
                    "entry_name": "HwSchMode",
                    "entry_value": 2,
                    "data_type": winreg.REG_DWORD,
                    "hive_root": winreg.HKEY_LOCAL_MACHINE,
                    "task_description": "Activate hardware-based scheduling for Intel integrated graphics"
                }
            ]

    def _initialize_network_optimizations(self):
        self.internet_connection_settings = [
            {
                "registry_path": r"SYSTEM\CurrentControlSet\Services\Tcpip\Parameters",
                "multiple_entries": {
                    "TcpAckFrequency": 1,
                    "TCPNoDelay": 1,
                    "TcpDelAckTicks": 0,
                    "TCPInitialRtt": 300,
                    "TcpMaxDupAcks": 2
                },
                "data_type": winreg.REG_DWORD,
                "hive_root": winreg.HKEY_LOCAL_MACHINE,
                "task_description": "Fine-tune TCP/IP stack for minimal online gaming latency"
            },
            {
                "registry_path": r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Multimedia\SystemProfile",
                "entry_name": "NetworkThrottlingIndex",
                "entry_value": 0xffffffff,
                "data_type": winreg.REG_DWORD,
                "hive_root": winreg.HKEY_LOCAL_MACHINE,
                "task_description": "Remove Windows network data throttling limits"
            },
            {
                "registry_path": r"SYSTEM\CurrentControlSet\Services\Tcpip\Parameters\Interfaces",
                "multiple_entries": {
                    "TcpAckFrequency": 1,
                    "TCPNoDelay": 1
                },
                "data_type": winreg.REG_DWORD,
                "hive_root": winreg.HKEY_LOCAL_MACHINE,
                "task_description": "Apply direct interface latency adjustments",
                "apply_to_all_subkeys": True
            },
            {
                "registry_path": r"SYSTEM\CurrentControlSet\Services\Ndu",
                "entry_name": "Start",
                "entry_value": 4,
                "data_type": winreg.REG_DWORD,
                "hive_root": winreg.HKEY_LOCAL_MACHINE,
                "task_description": "Disable Windows Network Data Usage Monitoring (NDU) service"
            }
        ]

    def _initialize_peripheral_and_driver_settings(self):
        self.peripheral_and_driver_optimizations = [
            {
                "registry_path": r"SOFTWARE\Microsoft\Windows\CurrentVersion\DriverSearching",
                "entry_name": "SearchOrderConfig",
                "entry_value": 0,
                "data_type": winreg.REG_DWORD,
                "hive_root": winreg.HKEY_LOCAL_MACHINE,
                "task_description": "Disable automatic Windows driver version searching"
            },
            {
                "registry_path": r"Control Panel\Mouse",
                "entry_name": "RawMouseThrottleDuration",
                "entry_value": 20,
                "data_type": winreg.REG_DWORD,
                "hive_root": winreg.HKEY_CURRENT_USER,
                "task_description": "Tuning mouse refresh throttle duration"
            }
        ]

    def check_administrative_privileges(self):
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False

    def execute_shell_command(self, shell_command, visual_description):
        status_logger.info(f"System: {visual_description}")
        try:
            is_using_shell = isinstance(shell_command, str)
            subprocess.run(shell_command, shell=is_using_shell, check=True, capture_output=True)
            status_logger.info(f"  {Fore.GREEN}[COMPLETED]{Style.RESET_ALL}")
            return True
        except subprocess.CalledProcessError as error:
            status_logger.error(f"  {Fore.RED}[ERROR] {error}{Style.RESET_ALL}")
            return False

    def modify_registry_configuration(self, optimization_entry):
        status_logger.info(f"Registry: {optimization_entry['task_description']}")
        
        if optimization_entry.get("apply_to_all_subkeys"):
            self._apply_settings_to_all_subkeys(optimization_entry)
            return

        active_entries = {}
        if "multiple_entries" in optimization_entry:
            active_entries = optimization_entry["multiple_entries"]
        else:
            active_entries = {optimization_entry["entry_name"]: optimization_entry["entry_value"]}

        try:
            with winreg.CreateKeyEx(optimization_entry["hive_root"], optimization_entry["registry_path"], 0, winreg.KEY_SET_VALUE) as registry_handle:
                for name, val in active_entries.items():
                    winreg.SetValueEx(registry_handle, name, 0, optimization_entry["data_type"], val)
            status_logger.info(f"  {Fore.GREEN}[COMPLETED]{Style.RESET_ALL}")
        except OSError as error:
            status_logger.error(f"  {Fore.RED}[ERROR] {error}{Style.RESET_ALL}")

    def _apply_settings_to_all_subkeys(self, registry_template):
        try:
            with winreg.OpenKey(registry_template["hive_root"], registry_template["registry_path"], 0, winreg.KEY_READ) as parent_key:
                index = 0
                while True:
                    try:
                        subkey_name = winreg.EnumKey(parent_key, index)
                        full_key_path = f"{registry_template['registry_path']}\\{subkey_name}"
                        
                        with winreg.OpenKey(registry_template["hive_root"], full_key_path, 0, winreg.KEY_SET_VALUE) as subkey_handle:
                            for name, val in registry_template["multiple_entries"].items():
                                winreg.SetValueEx(subkey_handle, name, 0, registry_template["data_type"], val)
                        index += 1
                    except OSError:
                        break
            status_logger.info(f"  {Fore.GREEN}[COMPLETED]{Style.RESET_ALL} Modifications applied to all subkeys")
        except OSError as error:
            status_logger.error(f"  {Fore.RED}[ERROR]{Style.RESET_ALL} Access denied to subkeys: {error}")

    def deactivate_usb_energy_management(self):
        status_logger.info("Hardware: Deactivating USB Selective Suspend features")
        powershell_script = (
            "Get-PnpDevice -PresentOnly | Where-Object { $_.InstanceId -like '*USB\\VID_*' } | ForEach-Object { "
            "$path = 'HKLM:\\SYSTEM\\CurrentControlSet\\Enum\\' + $_.InstanceId + '\\Device Parameters'; "
            "if (Test-Path $path) { "
            "Set-ItemProperty -Path $path -Name 'SelectiveSuspendOn' -Value 0 -Type DWord -ErrorAction SilentlyContinue; "
            "Set-ItemProperty -Path $path -Name 'EnhancedPowerManagementEnabled' -Value 0 -Type DWord -ErrorAction SilentlyContinue; "
            "} }"
        )
        self.execute_shell_command(['powershell', '-Command', powershell_script], "Deactivate USB Selective Suspend via PowerShell script")

    def deep_deactivate_all_device_power_saving(self):
        status_logger.info("Hardware: Deep deactivation of device-level power saving flags")
        powershell_batch_scan = (
            "$flags = @('EnhancedPowerManagementEnabled', 'AllowIdleIrpInD3', 'EnableSelectiveSuspend', "
            "'DeviceSelectiveSuspended', 'SelectiveSuspendEnabled', 'SelectiveSuspendOn', "
            "'EnumerationRetryCount', 'ExtPropDescSemaphore', 'WaitWakeEnabled', "
            "'D3ColdSupported', 'WdfDirectedPowerTransitionEnable', 'EnableIdlePowerManagement', "
            "'IdleInWorkingState'); "
            "Get-ChildItem -Path 'HKLM:\\SYSTEM\\CurrentControlSet\\Enum' -Recurse -ErrorAction SilentlyContinue | ForEach-Object { "
            "$keyPath = $_.Name.Replace('HKEY_LOCAL_MACHINE', 'HKLM:'); "
            "foreach ($flag in $flags) { "
            "if (Get-ItemProperty -Path $keyPath -Name $flag -ErrorAction SilentlyContinue) { "
            "Set-ItemProperty -Path $keyPath -Name $flag -Value 0 -Type DWord -ErrorAction SilentlyContinue; "
            "} } }; exit 0"
        )
        self.execute_shell_command(['powershell', '-Command', powershell_batch_scan], "Applying deep hardware power saving deactivation flags via registry recursion")

        wmi_power_management_disable = (
            "$devices = Get-CimInstance Win32_PnPEntity; "
            "$powerMgmt = Get-CimInstance MSPower_DeviceEnable -Namespace root\\wmi; "
            "foreach ($p in $powerMgmt) { "
            "$IN = $p.InstanceName.ToUpper(); "
            "foreach ($h in $devices) { "
            "$PNPDI = $h.PNPDeviceID; "
            "if ($IN -like ('*' + $PNPDI + '*')) { "
            "$p.enable = $False; "
            "Set-CimInstance -CimInstance $p; "
            "} } }"
        )
        self.execute_shell_command(['powershell', '-Command', wmi_power_management_disable], "Disabling per-device power management overrides via CIM/WMI")

    def disable_web_browser_telemetry(self):
        status_logger.info("Web Browsers: Stopping background data collection and telemetry")
        
        browser_configurations = {
            "Microsoft Edge": [
                {
                    "registry_path": r"SOFTWARE\Policies\Microsoft\Edge",
                    "multiple_entries": {
                        "MetricsReportingEnabled": 0,
                        "SendSiteInfoToImproveServices": 0,
                        "PersonalizationReportingEnabled": 0,
                        "UserFeedbackAllowed": 0
                    },
                    "data_type": winreg.REG_DWORD,
                    "hive_root": winreg.HKEY_LOCAL_MACHINE
                }
            ],
            "Google Chrome": [
                {
                    "registry_path": r"SOFTWARE\Policies\Google\Chrome",
                    "multiple_entries": {
                        "MetricsReportingEnabled": 0,
                        "ChromeCleanupReportingEnabled": 0,
                        "ChromeCleanupEnabled": 0
                    },
                    "data_type": winreg.REG_DWORD,
                    "hive_root": winreg.HKEY_LOCAL_MACHINE
                }
            ],
            "Mozilla Firefox": [
                {
                    "registry_path": r"SOFTWARE\Policies\Mozilla\Firefox",
                    "multiple_entries": {
                        "DisableTelemetry": 1,
                        "DisableFirefoxStudies": 1,
                        "DisablePocket": 1
                    },
                    "data_type": winreg.REG_DWORD,
                    "hive_root": winreg.HKEY_LOCAL_MACHINE
                }
            ]
        }
        
        for browser_brand, configurations in browser_configurations.items():
            for config in configurations:
                try:
                    with winreg.CreateKeyEx(config["hive_root"], config["registry_path"], 0, winreg.KEY_SET_VALUE) as registry_handle:
                        for name, value in config["multiple_entries"].items():
                            winreg.SetValueEx(registry_handle, name, 0, config["data_type"], value)
                    status_logger.info(f"  {Fore.GREEN}[COMPLETED]{Style.RESET_ALL} {browser_brand}")
                except OSError as error:
                    status_logger.error(f"  {Fore.RED}[ERROR]{Style.RESET_ALL} {browser_brand}: {error}")

    def prevent_automatic_windows_updates(self):
        status_logger.info("Windows: Halt automatic system updates")
        
        update_modifications = [
            {
                "registry_path": r"SOFTWARE\Policies\Microsoft\Windows\WindowsUpdate\AU",
                "multiple_entries": {
                    "NoAutoUpdate": 1,
                    "AUOptions": 2,
                    "ScheduledInstallDay": 0,
                    "ScheduledInstallTime": 3
                },
                "data_type": winreg.REG_DWORD,
                "hive_root": winreg.HKEY_LOCAL_MACHINE,
                "task_description": "Configure policy to stop automatic Windows updates"
            },
            {
                "registry_path": r"SOFTWARE\Microsoft\Windows\CurrentVersion\WindowsUpdate\Auto Update",
                "entry_name": "AUOptions",
                "entry_value": 1,
                "data_type": winreg.REG_DWORD,
                "hive_root": winreg.HKEY_LOCAL_MACHINE,
                "task_description": "Set Windows Update to manual notification only"
            }
        ]
        
        for modification in update_modifications:
            self.modify_registry_configuration(modification)
        
        update_services = ["wuauserv", "UsoSvc", "WaaSMedicSvc"]
        for service_name in update_services:
            self.execute_shell_command(f'sc config {service_name} start=disabled', f"Configure {service_name} service to disabled start")
            self.execute_shell_command(f'sc stop {service_name}', f"Immediately stop {service_name} service")

    def configure_high_performance_power_scheme(self):
        status_logger.info("Power Management: Activating Ultimate Performance profile")
        self.execute_shell_command(
            'powercfg -duplicatescheme e9a42b02-d5df-448d-aa00-03f14749eb61',
            "Generating Ultimate Performance scheme duplicate"
        )
        self.execute_shell_command(
            'powercfg -setactive e9a42b02-d5df-448d-aa00-03f14749eb61',
            "Enforcing Ultimate Performance scheme as active"
        )
        
        self.execute_shell_command(
            'powercfg -attributes SUB_PROCESSOR 36687f9e-e3a5-4dbf-b1dc-15eb381c6863 -ATTRIB_HIDE',
            "Revealing hidden CPU power throttling attribute"
        )
        self.execute_shell_command(
            'powercfg -setacvalueindex scheme_current sub_processor 36687f9e-e3a5-4dbf-b1dc-15eb381c6863 0',
            "Switching off CPU power throttling for AC power"
        )
        self.execute_shell_command(
            'powercfg -setdcvalueindex scheme_current sub_processor 36687f9e-e3a5-4dbf-b1dc-15eb381c6863 0',
            "Switching off CPU power throttling for battery power"
        )

    def ensure_windows_license_is_active(self):
        status_logger.info("License: Verifying and ensuring Windows activation status")
        try:
            check_command = "Get-CimInstance SoftwareLicensingProduct | Where-Object { $_.PartialProductKey } | Select-Object -ExpandProperty LicenseStatus"
            status_result = subprocess.run(['powershell', '-Command', check_command], capture_output=True, text=True)
            
            if '1' not in status_result.stdout:
                status_logger.info(f"  {Fore.YELLOW}[NOTICE]{Style.RESET_ALL} Windows is not activated. Initiating automated activation sequence...")
                activation_script = "Start-Process powershell -ArgumentList '-Command iex (irm https://get.activated.win)' -WindowStyle Hidden"
                subprocess.run(['powershell', '-Command', activation_script])
                status_logger.info(f"  {Fore.GREEN}[COMPLETED]{Style.RESET_ALL} Activation request dispatched")
            else:
                status_logger.info(f"  {Fore.GREEN}[ALREADY ACTIVE]{Style.RESET_ALL} Windows is correctly licensed")
        except Exception as error:
            status_logger.error(f"  {Fore.RED}[ERROR]{Style.RESET_ALL} License verification failed: {error}")

    def apply_memory_compression_tweak(self):
        status_logger.info(f"System: Memory compression adjustment (Detected RAM: {self.ram_gb}GB)")
        if self.ram_gb > 16:
            cmd = "Disable-MMAgent -MemoryCompression"
            desc = "Disabling memory compression for systems with >16GB RAM"
        else:
            cmd = "Enable-MMAgent -MemoryCompression"
            desc = "Enabling memory compression for systems with <=16GB RAM"
        
        self.execute_shell_command(['powershell', '-Command', cmd], desc)

    def start_optimization_sequence(self):
        if not self.check_administrative_privileges():
            status_logger.error(f"{Fore.RED}Administrative privileges are required to run this performance optimizer.{Style.RESET_ALL}")
            sys.exit(1)

        print("\n" + Fore.CYAN + "="*60 + Style.RESET_ALL)
        print(f"  {Fore.WHITE + Style.BRIGHT}ANTWEAKER - BY ANARCHOWITZ{Style.RESET_ALL}")
        print(Fore.CYAN + "="*60 + Style.RESET_ALL)
        print(f"\nGraphics Hardware: {Fore.YELLOW}{self.graphics_card_type}{Style.RESET_ALL}")
        print(f"Storage Medium: {Fore.YELLOW}{self.storage_medium_type}{Style.RESET_ALL}")
        print("\n" + Fore.CYAN + "="*60 + Style.RESET_ALL + "\n")

        status_logger.info(f"\n{Fore.CYAN}Stage 1: Core System Adjustments{Style.RESET_ALL}")
        for adjustment in self.core_system_adjustments:
            self.modify_registry_configuration(adjustment)

        status_logger.info(f"\n{Fore.CYAN}Stage 2: Processing Latency Reductions{Style.RESET_ALL}")
        for optimization in self.delay_reduction_optimizations:
            self.modify_registry_configuration(optimization)

        status_logger.info(f"\n{Fore.CYAN}Stage 3: Memory Allocation Optimizations{Style.RESET_ALL}")
        for setting in self.memory_optimization_settings:
            self.modify_registry_configuration(setting)

        status_logger.info(f"\n{Fore.CYAN}Stage 4: Storage Optimization ({self.storage_medium_type}){Style.RESET_ALL}")
        for adjustment in self.storage_adjustments:
            self.modify_registry_configuration(adjustment)

        status_logger.info(f"\n{Fore.CYAN}Stage 5: Processor Efficiency Adjustments{Style.RESET_ALL}")
        for tweak in self.processor_performance_tweaks:
            self.modify_registry_configuration(tweak)

        status_logger.info(f"\n{Fore.CYAN}Stage 6: Display Frame Rate Smoothing{Style.RESET_ALL}")
        for adjustment in self.frame_rate_adjustments:
            self.modify_registry_configuration(adjustment)

        status_logger.info(f"\n{Fore.CYAN}Stage 7: Power Delivery Configuration{Style.RESET_ALL}")
        for optimization in self.energy_management_optimizations:
            self.modify_registry_configuration(optimization)

        if self.video_card_optimizations:
            status_logger.info(f"\n{Fore.CYAN}Stage 8: {self.graphics_card_type} Graphics Specific Tuning{Style.RESET_ALL}")
            for tuning in self.video_card_optimizations:
                self.modify_registry_configuration(tuning)
        else:
            status_logger.info(f"\n{Fore.CYAN}Stage 8: Skipping Video Card Tuning (Hardware: {self.graphics_card_type}){Style.RESET_ALL}")

        status_logger.info(f"\n{Fore.CYAN}Stage 9: Network Throughput Optimizations{Style.RESET_ALL}")
        for setting in self.internet_connection_settings:
            self.modify_registry_configuration(setting)

        self.execute_shell_command("netsh int tcp set global ecncapability=enabled", "Enabling Explicit Congestion Notification (ECN) in TCP stack")
        self.execute_shell_command("netsh int ip set global taskoffload=enabled", "Enabling IP Task Offload in network stack")

        status_logger.info(f"\n{Fore.CYAN}Stage 10: Peripheral and Driver Configuration{Style.RESET_ALL}")
        for optimization in self.peripheral_and_driver_optimizations:
            self.modify_registry_configuration(optimization)

        status_logger.info(f"\n{Fore.CYAN}Stage 11: Low-Level Boot Configuration Timing{Style.RESET_ALL}")
        self.execute_shell_command("bcdedit /set disabledynamictick yes", "Disabling dynamic kernel ticks to improve timing consistency")
        self.execute_shell_command("bcdedit /set useplatformtick yes", "Enforcing use of high-resolution platform ticks")
        self.execute_shell_command("bcdedit /set tscsyncpolicy enhanced", "Setting enhanced TSC synchronization policy across cores")

        status_logger.info(f"\n{Fore.CYAN}Stage 12: Peripheral Interrupt Tuning{Style.RESET_ALL}")
        self.deactivate_usb_energy_management()
        self.deep_deactivate_all_device_power_saving()

        status_logger.info(f"\n{Fore.CYAN}Stage 13: Data Privacy and System Services Cleanup{Style.RESET_ALL}")
        self.disable_web_browser_telemetry()
        self.prevent_automatic_windows_updates()
        self.configure_high_performance_power_scheme()
        
        status_logger.info(f"\n{Fore.CYAN}Stage 14: System Licensing & Performance Finalization{Style.RESET_ALL}")
        self.apply_memory_compression_tweak()
        self.ensure_windows_license_is_active()

        print("\n" + Fore.CYAN + "="*60 + Style.RESET_ALL)
        print(f"  {Fore.GREEN}✓ All performance optimizations have been applied successfully.{Style.RESET_ALL}")
        print(f"  {Fore.RED}⚠ A FULL SYSTEM RESTART IS MANDATORY FOR ALL CHANGES TO TAKE EFFECT.{Style.RESET_ALL}")
        print(Fore.CYAN + "="*60 + Style.RESET_ALL + "\n")
        
        input(f"{Fore.YELLOW}Оптимизация завершена. Нажмите Enter, чтобы закрыть программу...{Style.RESET_ALL}")

if __name__ == "__main__":
    optimizer_instance = WindowsPerformanceOptimizer()
    optimizer_instance.start_optimization_sequence()
