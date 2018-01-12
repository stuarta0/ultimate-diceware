for fileSource in *.svg
do
    if [ -f "$fileSource" ]; then    
        count=$((count+1))
        file=$(echo $fileSource | cut -d'.' -f1)
        echo $count". "$fileSource" -> "$file.pdf
        inkscape $fileSource --export-pdf=$file.pdf --export-dpi=$dpi
    else
        echo "no file $fileSource found!"
    fi
done
echo "$count file(s) converted!"
