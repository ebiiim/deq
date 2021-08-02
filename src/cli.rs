use std::io::stdin;
use std::io::{stdout, Write};
use std::process;

use crate::err::DeqError;

fn get_device_names(pa: &portaudio::PortAudio) -> Result<Vec<(usize, String)>, DeqError> {
    log::trace!("get devices");
    let devs = pa.devices();
    match devs {
        Ok(devs) => Ok(devs
            .map(|dev| {
                let d = dev.unwrap();
                let portaudio::DeviceIndex(idx) = d.0;
                (idx as usize, String::from(d.1.name))
            })
            .collect()),
        Err(_) => Err(DeqError::InvalidDevice),
    }
}

fn print_devices(pa: &portaudio::PortAudio) -> Result<(), DeqError> {
    let device_names = get_device_names(pa)?;
    device_names.iter().all(|(idx, name)| {
        println!("{}\t{}", idx, name);
        true
    });
    Ok(())
}

fn get_device_info(
    pa: &portaudio::PortAudio,
    idx: usize,
) -> Result<portaudio::DeviceInfo, DeqError> {
    let devidx = portaudio::DeviceIndex(idx as u32);
    log::trace!("get devices");
    let devs = pa.devices();
    if let Ok(devs) = devs {
        for d in devs {
            if let Ok(d) = d {
                if d.0 == devidx {
                    return Ok(d.1);
                }
            } else {
                return Err(DeqError::InvalidDevice);
            }
        }
    }
    Err(DeqError::InvalidDevice)
}

fn print_device_info(pa: &portaudio::PortAudio, idx: usize) -> Result<(), DeqError> {
    let devinfo = get_device_info(pa, idx)?;
    println!("{:#?}", devinfo);
    Ok(())
}

fn read_str(s: &str) -> Result<String, DeqError> {
    print!("{}", s);
    if stdout().flush().is_err() {
        log::error!("could not flush stdout");
    }
    let mut input = String::new();
    if stdin().read_line(&mut input).is_err() {
        log::error!("could not read line");
        return Err(DeqError::InvalidOperation);
    }
    log::trace!("read_str={}", input);
    Ok(input)
}

fn read_int(s: &str) -> Result<usize, DeqError> {
    let read = read_str(s)?.trim().parse();
    log::trace!("read_int={:?}", read);
    match read {
        Ok(i) => Ok(i),
        Err(_) => Err(DeqError::InvalidOperation),
    }
}

pub fn select_devices_loop(pa: &portaudio::PortAudio) -> (usize, usize) {
    let term_clear = || print!("\x1B[2J");
    let term_left_top = || print!("\x1B[1;1H");
    let no_dev = 1 << 31;

    let mut input_dev = no_dev;
    let mut output_dev = no_dev;

    term_clear();
    term_left_top();

    loop {
        if input_dev != no_dev && output_dev != no_dev {
            break;
        }
        let cmd = read_int("Command(0:devices,1:detail,2:input,3:output,9:exit)>");
        match cmd {
            Err(_) => {
                continue;
            }
            Ok(cmd) => {
                if cmd == 0 {
                    println!("PortAudio version: {}", portaudio::version());
                    let dc = pa.device_count();
                    if dc.is_err() {
                        log::error!("could not fetch devices");
                        continue;
                    }
                    println!("Device count: {}", dc.unwrap());
                    if print_devices(pa).is_err() {
                        log::error!("could not print devices");
                    }
                } else if cmd == 1 {
                    if let Ok(n) = read_int("see device> ") {
                        if print_device_info(pa, n).is_err() {
                            log::error!("could not find device id={}", n);
                        }
                    }
                } else if cmd == 2 {
                    if let Ok(n) = read_int("input device> ") {
                        if get_device_info(pa, n).is_ok() {
                            input_dev = n;
                        } else {
                            log::error!("could not find device id={}", n);
                        }
                    }
                } else if cmd == 3 {
                    if let Ok(n) = read_int("output device> ") {
                        if get_device_info(pa, n).is_ok() {
                            output_dev = n;
                        } else {
                            log::error!("could not find device id={}", n);
                        }
                    }
                } else if cmd == 9 {
                    log::debug!("exit");
                    process::exit(0);
                } else {
                    log::debug!("invalid command");
                    continue;
                }
            }
        }
    }
    log::debug!(
        "devices selected input={}, output={}",
        input_dev,
        output_dev
    );
    (input_dev, output_dev)
}
