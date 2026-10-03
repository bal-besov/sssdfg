import json
import subprocess
import sys


DDR_TYPES = {
    0: "Неизвестно",
    20: "DDR",
    21: "DDR2",
    22: "DDR2 FB-DIMM",
    24: "DDR3",
    26: "DDR4",
    27: "LPDDR",
    28: "LPDDR2",
    29: "LPDDR3",
    30: "LPDDR4",
    34: "DDR5",
    35: "LPDDR5",
}


def powershell_json(command: str):
    """Выполняет PowerShell-команду и возвращает разобранный JSON."""
    script = (
        "[Console]::OutputEncoding = [System.Text.Encoding]::UTF8; "
        f"{command} | ConvertTo-Json -Depth 5 -Compress"
    )

    result = subprocess.run(
        ["powershell.exe", "-NoProfile", "-Command", script],
        capture_output=True,
        encoding="utf-8",
        errors="replace",
    )

    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip())

    output = result.stdout.strip()
    return json.loads(output) if output else None


def as_list(value):
    """PowerShell возвращает объект вместо массива, если элемент только один."""
    if value is None:
        return []
    return value if isinstance(value, list) else [value]


def gb(value):
    return round(int(value or 0) / 1024**3, 2)


def main():
    cpu = as_list(
        powershell_json(
            "Get-CimInstance Win32_Processor | "
            "Select-Object Name,NumberOfCores,NumberOfLogicalProcessors,MaxClockSpeed"
        )
    )

    gpu = as_list(
        powershell_json(
            "Get-CimInstance Win32_VideoController | "
            "Select-Object Name,DriverVersion,AdapterRAM"
        )
    )

    motherboard = as_list(
        powershell_json(
            "Get-CimInstance Win32_BaseBoard | "
            "Select-Object Manufacturer,Product,Version"
        )
    )

    ram = as_list(
        powershell_json(
            "Get-CimInstance Win32_PhysicalMemory | "
            "Select-Object DeviceLocator,Manufacturer,PartNumber,Capacity,"
            "ConfiguredClockSpeed,Speed,SMBIOSMemoryType"
        )
    )

    print("\n=== ПРОЦЕССОР ===")
    for item in cpu:
        print(f"Модель:             {item.get('Name', '').strip()}")
        print(f"Ядра / потоки:      {item.get('NumberOfCores')} / "
              f"{item.get('NumberOfLogicalProcessors')}")
        print(f"Макс. частота:      {item.get('MaxClockSpeed')} МГц")

    print("\n=== ВИДЕОКАРТА ===")
    for index, item in enumerate(gpu, 1):
        print(f"{index}. {item.get('Name')}")
        print(f"   Драйвер:         {item.get('DriverVersion')}")

        # AdapterRAM иногда определяется неправильно для современных GPU.
        adapter_ram = item.get("AdapterRAM")
        if adapter_ram:
            print(f"   Видеопамять:     {gb(adapter_ram)} ГБ")

    print("\n=== МАТЕРИНСКАЯ ПЛАТА ===")
    for item in motherboard:
        print(f"Производитель:      {item.get('Manufacturer')}")
        print(f"Модель:             {item.get('Product')}")
        print(f"Версия:             {item.get('Version')}")

    print("\n=== ОПЕРАТИВНАЯ ПАМЯТЬ ===")
    print(f"Общий объём:        {sum(gb(x.get('Capacity')) for x in ram):g} ГБ")

    detected_types = set()

    for index, item in enumerate(ram, 1):
        type_code = int(item.get("SMBIOSMemoryType") or 0)
        memory_type = DDR_TYPES.get(type_code, f"SMBIOS-код {type_code}")
        detected_types.add(memory_type)

        clock = (
            item.get("ConfiguredClockSpeed")
            or item.get("Speed")
            or "неизвестно"
        )

        print(f"\nМодуль {index}:")
        print(f"  Слот:             {item.get('DeviceLocator')}")
        print(f"  Тип:              {memory_type}")
        print(f"  Объём:            {gb(item.get('Capacity'))} ГБ")
        print(f"  Частота:          {clock} МГц")
        print(f"  Производитель:    {item.get('Manufacturer')}")
        print(f"  Артикул:          {(item.get('PartNumber') or '').strip()}")

    print("\nТип установленной памяти:", ", ".join(sorted(detected_types)))


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print(f"Ошибка: {error}", file=sys.stderr)
        sys.exit(1)
