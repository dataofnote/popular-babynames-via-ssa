# This was written awhile ago and doesn't follow my more
# sane, modern conventions...

require 'pathname'
require 'shellwords'
require 'shell'
include Shellwords

WRANGLE_DIR = Pathname 'wrangle'
SCRIPTS_DIR = WRANGLE_DIR.join('scripts')
DIRS = {
    :fetched_nationwide => WRANGLE_DIR.join('corral', 'fetched', 'nationwide'),
    :fetched_states => WRANGLE_DIR.join('corral', 'fetched', 'states'),
    :compiled => WRANGLE_DIR.join('corral', 'compiled'),
    :supplemented => WRANGLE_DIR.join('corral', 'supplemented'),
    :published =>  Pathname('catalog'),
}

START_YEAR = 1880
END_YEAR = 2015
STATE_ABBREVS = %w(AK AL AR AZ CA CO CT DC DE FL GA HI IA ID IL IN KS KY LA MA MD ME MI MN MO MS MT NC ND NE NH NJ NM NV NY OH OK OR PA RI SC SD TN TX UT VA VT WA WI WV WY)

FILES = {
    fetched_nationwide: (START_YEAR..END_YEAR).map{|y| DIRS[:fetched_nationwide].join("yob#{y}.txt")},
    fetched_states: STATE_ABBREVS.map{|s| DIRS[:fetched_states].join("#{s}.TXT")},
    compiled_nationwide: DIRS[:compiled].join("nationwide.csv"),
    compiled_states: DIRS[:compiled].join("states.csv"),
    compiled_all: DIRS[:compiled].join("all.csv"),
    ranks_ratios: DIRS[:supplemented].join('ranks-ratios.csv'),
    name_aggregates: DIRS[:supplemented].join('name-aggregates.csv'),
}

PUB_FILES = {
    complete: 'ssa-babynames.csv',
    since_1950: 'ssa-babynames-since-1950.csv',
    since_1980: 'ssa-babynames-since-1980.csv',
    p2000_2015: 'ssa-babynames-2000-through-2015.csv',
    nationwide: 'ssa-babynames-nationwide.csv',
    nationwide_since_1950: 'ssa-babynames-nationwide-since-1950.csv',
    nationwide_since_1980: 'ssa-babynames-nationwide-since-1980.csv',
    nationwide_2000_2015: 'ssa-babynames-nationwide-2000-through-2015.csv',
    nationwide_top_10: "ssa-babynames-nationwide-annual-top-10.csv",
    top_10: "ssa-babynames-annual-top-10.csv",
}

PUB_FILES.each_pair{|k, v| PUB_FILES[k] = DIRS[:published].join(v)}



shell = Shell.new

desc 'Setup the directories'
task :setup do
    DIRS.each_value do |p|
        p.mkpath()
        puts "Created directory: #{p}"
    end
end

namespace :package do
    desc "Download and save the nationwide and states data"
    task :fetch do
        Rake::Task['fetch:nationwide'].execute
        Rake::Task['fetch:states'].execute
    end

    desc "Compile data into one file with common headers"
    task :compile do
        Rake::Task[FILES[:compiled_all]].invoke
    end
end



namespace :fetch do
    desc "Fetch nationwide zip file"
    task :nationwide do
        cmd = shelljoin(['python', SCRIPTS_DIR.join('fetch_and_unpack_data.py'),
                               'nationwide', DIRS[:fetched_nationwide]])
        puts shell.system(cmd)
    end

    desc "Fetch states zip file"
    task :states do
        cmd = shelljoin(['python', SCRIPTS_DIR.join('fetch_and_unpack_data.py'),
                               'states', DIRS[:fetched_states]])
        puts shell.system(cmd)
    end
end


################################
# Files and their dependencies



desc "Complete data to be published; all years, all states"
file PUB_FILES[:complete] => FILES[:ranks_ratios] do
    sh "cp #{FILES[:ranks_ratios]} #{PUB_FILES[:complete]}"
end


desc "Data from 1950"
file PUB_FILES[:since_1950] => PUB_FILES[:complete] do
    sh [
        "python",
        SCRIPTS_DIR.join('filter_columns.py'),
        PUB_FILES[:complete],
        "--start-year 1950",
        ">",
        PUB_FILES[:since_1950],
       ].join(' ')
end


desc "Data from 1980"
file PUB_FILES[:since_1980] => PUB_FILES[:since_1950] do
    sh [
        "python",
        SCRIPTS_DIR.join('filter_columns.py'),
        PUB_FILES[:since_1950],
        "--start-year 1980",
        ">",
        PUB_FILES[:since_1980],
       ].join(' ')
end

desc "Data from 2000 through 2015"
file PUB_FILES[:p2000_2015] => PUB_FILES[:since_1980] do
    sh [
        "python",
        SCRIPTS_DIR.join('filter_columns.py'),
        PUB_FILES[:since_1980],
        "--start-year 2000",
        "--end-year 2015",
        ">",
        PUB_FILES[:p2000_2015],
       ].join(' ')
end




desc "Nationwide-data only"
file PUB_FILES[:nationwide] => PUB_FILES[:complete] do
    sh [
        "python",
        SCRIPTS_DIR.join('filter_columns.py'),
        PUB_FILES[:complete],
        "--states US",
        ">",
        PUB_FILES[:nationwide],
       ].join(' ')
end

desc "Nationwide-data since 1950"
file PUB_FILES[:nationwide_since_1950] => PUB_FILES[:nationwide] do
    sh [
        "python",
        SCRIPTS_DIR.join('filter_columns.py'),
        PUB_FILES[:nationwide],
        "--start-year 1950",
        "--states US",
        ">",
        PUB_FILES[:nationwide_since_1950],
       ].join(' ')
end

desc "Nationwide-data since 1980"
file PUB_FILES[:nationwide_since_1980] => PUB_FILES[:nationwide_since_1950] do
    sh [
        "python",
        SCRIPTS_DIR.join('filter_columns.py'),
        PUB_FILES[:nationwide_since_1950],
        "--start-year 1980",
        "--states US",
        ">",
        PUB_FILES[:nationwide_since_1980],
       ].join(' ')
end


desc "Data from 2000 through 2015"
file PUB_FILES[:nationwide_2000_2015] => PUB_FILES[:nationwide_since_1980] do
    sh [
        "python",
        SCRIPTS_DIR.join('filter_columns.py'),
        PUB_FILES[:nationwide_since_1980],
        "--start-year 2000",
        "--end-year 2015",
        ">",
        PUB_FILES[:nationwide_2000_2015],
       ].join(' ')
end



desc "Top 10 names per year, state, and sex"
file PUB_FILES[:top_10] => PUB_FILES[:complete] do
    sh [
        "python",
        SCRIPTS_DIR.join('filter_columns.py'),
        PUB_FILES[:complete],
        "--rank 10",
        ">",
        PUB_FILES[:top_10],
       ].join(' ')
end

desc "Top 10 names per year, state, and sex by nation"
file PUB_FILES[:nationwide_top_10] => PUB_FILES[:top_10] do
    sh [
        "python",
        SCRIPTS_DIR.join('filter_columns.py'),
        PUB_FILES[:top_10],
        "--states US",
        ">",
        PUB_FILES[:nationwide_top_10],
       ].join(' ')
end







### Intermediate files



desc "Rankings, ratios of names, regardless of sex"
file FILES[:name_aggregates] => FILES[:compiled_all] do
    sh %Q{python #{SCRIPTS_DIR.join('calculate_rank_ratio_by_name.py')} \
              #{FILES[:compiled_all]} \
            > #{FILES[:name_aggregates]}
        }
end


desc "Rankings, ratios of names, within sexes"
file FILES[:ranks_ratios] => FILES[:compiled_all] do
    sh """python #{SCRIPTS_DIR.join('calculate_rank_ratio.py')} \
              #{FILES[:compiled_all]} \
            > #{FILES[:ranks_ratios]}"""
end

desc "Put nationwide and states into one file"
file FILES[:compiled_all] => [FILES[:compiled_nationwide], FILES[:compiled_states]] do
    sh "cat #{FILES[:compiled_states]} > #{FILES[:compiled_all]}"
    # FreeBSD tail is much slower than the sed variant, not so if on GNU...
    sh "sed '1d' #{FILES[:compiled_nationwide]} >> #{FILES[:compiled_all]}"
end


desc "Compile nationwide CSV file, for years #{START_YEAR} through #{END_YEAR}"
file FILES[:compiled_nationwide] => FILES[:fetched_nationwide] do
    cmd = shelljoin(['python',
        SCRIPTS_DIR.join('compile_data.py'),
        'nationwide',
        DIRS[:fetched_nationwide]])
    shell.system(cmd) > FILES[:compiled_nationwide].to_s
end


desc 'Compile states CSV file'
file FILES[:compiled_states] => FILES[:fetched_states] do
    cmd = shelljoin(['python',
        SCRIPTS_DIR.join('compile_data.py'),
        'states',
        DIRS[:fetched_states]])
    shell.system(cmd) > FILES[:compiled_states].to_s
end


