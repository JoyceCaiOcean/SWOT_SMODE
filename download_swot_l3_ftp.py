import ftplib

ftp = ftplib.FTP('ftp-access.aviso.altimetry.fr')
ftp.login('joycecai@uw.edu','qeiQLd')

save_dir = 'SWOT_l3_expert/'

for ic in range(474,579):
    
    ftp.cwd(f'/swot_products/l3_karin_nadir/l3_lr_ssh/v1_0/Expert/cycle_{ic}')

    files = ftp.nlst()

    for i, f in enumerate(files):
        YYY = f[26:29]
        if (YYY=='013') | (YYY=='026'):
            print(f'{ic}')
            with open(save_dir+f, 'wb') as local_file:
                ftp.retrbinary('RETR '+f, local_file.write)

ftp.quit()