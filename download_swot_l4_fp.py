import ftplib

ftp = ftplib.FTP('ftp-access.aviso.altimetry.fr')
ftp.login('joycecai@uw.edu','qeiQLd')

save_dir = 'SWOT_l4/'


    
ftp.cwd(f'/duacs-experimental/dt-phy-grids/l4_karin_nadir/miost/calval')
files = ftp.nlst()

for i, f in enumerate(files):
    progress = 100*i/len(files)
    if i%100==0:
        print(f'{progress}%')
    with open(save_dir+f, 'wb') as local_file:
            ftp.retrbinary('RETR '+f, local_file.write)

ftp.quit()
