# Mass Flow rate readout for MFCs to get a constant readout of flow rates
import asyncio
from alicat import FlowController

# Mass Flow rate readout for MFCs to get a constant readout of flow rates
import asyncio
from alicat import FlowController

def read_flow_rates():
    # Run the asynchronous batch read function
    values = asyncio.run(read_all_flow_rates_async())
    try:
        # Ensure all values are floats and return them as a tuple
        return tuple(float(value) for value in values)
    except (TypeError, ValueError):
        # Return (0.0, 0.0, 0.0) if any value is invalid
        return (0.0, 0.0, 0.0)

async def read_all_flow_rates_async():
    try:
        # Create FlowController instances for all three MFCs
        async with FlowController(address='COM3', unit='A') as mfcA, \
                   FlowController(address='COM3', unit='B') as mfcB, \
                   FlowController(address='COM3', unit='C') as mfcC:
            # Gather all readouts concurrently, handling exceptions individually
            results = await asyncio.gather(
                safe_get_mass_flow(mfcA, 'A'),
                safe_get_mass_flow(mfcB, 'B'),
                safe_get_mass_flow(mfcC, 'C'),
                return_exceptions=True  # Allow individual exceptions
            )

            # Process results: return 0.0 for errors, valid values otherwise
            flow_rates = tuple(
                result if not isinstance(result, Exception) else 0.0
                for result in results
            )
            return flow_rates
    except Exception as e:
        # If something unexpected happens, return 0.0 for all
        print(f"Unexpected error in read_all_flow_rates_async: {e}")
        return (0.0, 0.0, 0.0)

async def safe_get_mass_flow(mfc, unit):
    try:
        data = await mfc.get()
        return data.get('mass_flow', 0.0)  # Default to 0.0 if 'mass_flow' is missing
    except Exception as e:
        print(f"Error reading mass flow for MFC {unit}: {e}")
        return 0.0  # Return 0.0 for errors