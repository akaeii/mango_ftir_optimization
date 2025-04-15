import pandas as pd
import glob
import os


def mdi_compute(input_dir: str, output_path: str):
    os.makedirs(output_path, exist_ok=True)

    # Loading Data
    csv_paths = glob.glob(f"{input_dir}/*_scans.csv")
    wave_no = pd.read_csv(f"{input_dir}/wavenumber.csv")

    scan_no_dict = {
        path.split("\\")[-1].replace(".csv", ""): pd.read_csv(path)
        for path in csv_paths
    }

    # Computing MDI
    lp = 3996.73391
    rp = 599.51009
    i = wave_no["wavenumber"]

    result_df = pd.DataFrame()

    for key, df in scan_no_dict.items():

        mdi_results = []

        for sample in df.columns:
            p = df[sample]
            md_lp = sum(((p**2) + ((i - lp)) ** 2) ** 0.5)
            md_rp = sum(((p**2) + ((rp - i)) ** 2) ** 0.5)
            mdi = md_rp - md_lp
            mdi_results.append(mdi)

        result_df[f"{key}_mdi"] = pd.Series(mdi_results)

    result_df.to_csv(f"{output_path}/master_mdi.csv", index=False)


def smdi_compute(input_dir: str, output_path: str):
    os.makedirs(output_path, exist_ok=True)

    # Loading Data
    master_mdi_path = glob.glob(f"{input_dir}/master_mdi.csv")
    master_mdi = pd.read_csv(master_mdi_path[0])

    # Computing SMDI
    result_df = pd.DataFrame()

    scan_n_max = master_mdi.max()
    scan_n_min = master_mdi.min()

    global_max = scan_n_max.max()
    global_min = scan_n_min.min()

    mdi_range = global_max - global_min

    for col in master_mdi.columns:
        smdi = (master_mdi[col] - global_min) / (mdi_range)
        result_df[col] = pd.Series(smdi)

    result_df.to_csv(f"{output_path}/master_smdi.csv", index=False)


if __name__ == "__main__":
    pass
