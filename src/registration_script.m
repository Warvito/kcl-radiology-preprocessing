% Function to preprocess the radiological images using RunPreproc

[fid, error_msg] = fopen('/tmp/image_files.txt', 'r');
if fid == -1
    error('Could not open /tmp/image_files.txt.\nSystem error message:\n%s\n', error_msg)
end
image_files = textscan(fid, '%s');
fclose(fid);

[fid, error_msg] = fopen('/tmp/output_dir.txt', 'r');
if fid == -1
    error('Could not open /tmp/output_dir.txt.\nSystem error message:\n%s\n', error_msg)
end
output_dir = fgetl(fid);
fclose(fid);

[fid, error_msg] = fopen('/tmp/use_coregistration.txt', 'r');
if fid == -1
    error('Could not open /tmp/use_coregistration.txt.\nSystem error message:\n%s\n', error_msg)
end
use_coregistration = fgetl(fid);
fclose(fid);

[fid, error_msg] = fopen('/tmp/use_labels.txt', 'r');
if fid == -1
    error('Could not open /tmp/use_labels.txt.\nSystem error message:\n%s\n', error_msg)
end
use_labels = fgetl(fid);
fclose(fid);

if strcmp(use_labels,'true')
    [fid, error_msg] = fopen('/tmp/label_files.txt', 'r');
    if fid == -1
        error('Could not open /tmp/label_files.txt.\nSystem error message:\n%s\n', error_msg)
    end
    label_files = textscan(fid, '%s');
    fclose(fid);
end

% Set preprocessing options
opt = struct;
opt.do.coreg = false;
opt.do.real_mni = true;
opt.do.crop = true;
opt.crop.keep_neck = false;
opt.do.vx = true;
opt.vx.size = 1;
opt.do.bb_spm = true;
opt.realign2mni.rigid = false; % false => full affine transformation
opt.do.segment = false;
opt.do.skullstrip = false;
opt.do.bfcorr = false;
opt.do.reslice = false;
opt.do.superres = false;
opt.do.denoise = false;
opt.segment.write_df = [0 0];
opt.do.res_orig = true;
opt.prefix = '';
opt.do.writemat = true;
opt.dir_out = output_dir;

if strcmp(use_coregistration,'true')
    opt_current.do.coreg = true;
elseif strcmp(use_coregistration,'false')
    opt_current.do.coreg = false;
end

if strcmp(use_labels,'true')
    RunPreproc({image_files, label_files}, opt)
else
    RunPreproc(image_files, opt)
end
