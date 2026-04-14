import os 
from pathlib import Path
import argparse
from string import Template
import pwd

def setup():
    t2_local_prefix = "/eos/uscms/"
    t2_prefix = "root://cmseos.fnal.gov"
    
    proxy = '/uscms/home/ammitra/x509up_u56971'

    username = os.environ["USER"]
    submitdir = Path(__file__).resolve().parent

    return t2_local_prefix, t2_prefix, proxy, username, submitdir

def write_template(templ_file: str, out_file: Path, templ_args: dict, safe: bool = False):
    """Write to ``out_file`` based on template from ``templ_file`` using ``templ_args``"""
    with Path(templ_file).open() as f:
        templ = Template(f.read())
    with Path(out_file).open("w") as f:
        if not safe:
            f.write(templ.substitute(templ_args))
        else:
            f.write(templ.safe_substitute(templ_args))

def main(ijob, njobs, nEvents):
    t2_local_prefix, t2_prefix, proxy, username, submitdir = setup()
    prefix    = f"step1_job{ijob}of{njobs}"
    path      = f"logs/{prefix}"
    local_dir = Path(path)
    # make local directory for output
    logdir = local_dir / "logs"
    logdir.mkdir(parents=True, exist_ok=True)

    jdl_templ = f"{submitdir}/submit_step1.templ.jdl"
    sh_templ  = f"{submitdir}/submit_step1.templ.sh"

    local_jdl = Path(f'{local_dir}/{prefix}.jdl')
    local_log = Path(f'{local_dir}/{prefix}.log')

    # JDL arguments
    jdl_args = {
        'dir': local_dir,
        'prefix': prefix,
        'user': pwd.getpwuid(os.getuid())[0],
        'i': ijob
    }
    write_template(jdl_templ, local_jdl, jdl_args)

    # shell script args
    localsh = f'{local_dir}/{prefix}.sh'
    sh_args = {
        'nEvents': nEvents,
        'i': ijob
    }
    write_template(sh_templ, localsh, sh_args, safe=True)

    # make executable
    os.system(f"chmod u+x {localsh}")

    if local_log.exists():
        local_log.unlink()

    os.system(f"condor_submit {local_jdl}")
    print("To submit ", local_jdl)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--nEvents', help='Number of events per job', type=int, default=100)
    parser.add_argument('--nJobs', help='Number of jobs to run', type=int, default=100)
    args = parser.parse_args()
    print(f'Generating {args.nEvents*args.nJobs} events over {args.nJobs} jobs....')
    for i in range(args.nJobs):
        main(i+1, args.nJobs, args.nEvents)
