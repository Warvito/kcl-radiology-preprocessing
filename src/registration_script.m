% Function to preprocess the radiological images using RunPreproc

[fid, error_msg] = fopen('/tmp/input_files.txt', 'r');
if fid == -1
    error('Could not open /tmp/input_files.txt.\nSystem error message:\n%s\n', error_msg)
end
input_image = textscan(fid, '%s');
fclose(fid);

[fid, error_msg] = fopen('/tmp/output_dir.txt', 'r');
if fid == -1
    error('Could not open /tmp/output_dir.txt.\nSystem error message:\n%s\n', error_msg)
end
output_dir = fgetl(fid);
fclose(fid);

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

opt.dir_out = output_dir;

if length(input_image) > 1 && index_of_t1s(k)
    opt_current.do.coreg = true;
end

RunPreproc(input_image, opt)
