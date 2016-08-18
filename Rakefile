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
    :published =>  Pathname('data'),
}

START_YEAR = 1880
END_YEAR = 2015
STATE_ABBREVS = %w(AK AL AR AZ CA CO CT DC DE FL GA HI IA ID IL IN KS KY LA MA MD ME MI MN MO MS MT NC ND NE NH NJ NM NV NY OH OK OR PA RI SC SD TN TX UT VA VT WA WI WV WY)

FETCHED_NATIONFILES = (START_YEAR..END_YEAR).map{|y| DIRS[:fetched_nationwide].join("yob#{y}.txt")}
FETCHED_STATEFILES = STATE_ABBREVS.map{|s| DIRS[:fetched_states].join("#{s}.TXT")}
COMPILED_FILES = [:all, :nationwide, :states].inject({}){|h, x| h[x] = DIRS[:compiled].join("#{x}.csv"); h }


shell = Shell.new

desc 'Setup the directories'
task :setup do
    DIRS.each_value do |p|
        p.mkpath()
        puts "Created directory: #{p}"
    end
end

namespace :package do
    desc "Fetch all the data"
    task :fetch do
        Rake::Task['fetch:nationwide'].execute
        Rake::Task['fetch:states'].execute
    end

    desc "Compile data into one file with common headers"
    task :compile do
        Rake::Task[COMPILED_FILES[:all]].invoke
    end
end



namespace :fetch do
    desc "Fetch nationwide zip file"
    task :nationwide do
        cmd = shelljoin(['python', SCRIPTS_DIR.join('fetch_and_unpack.py'),
                               'nationwide', DIRS[:fetched_nationwide]])
        puts shell.system(cmd)
    end

    desc "Fetch states zip file"
    task :states do
        cmd = shelljoin(['python', SCRIPTS_DIR.join('fetch_and_unpack.py'),
                               'states', DIRS[:fetched_states]])
        puts shell.system(cmd)
    end
end


desc "Put nationwide and states into one file"
file COMPILED_FILES[:all] => [COMPILED_FILES[:nationwide], COMPILED_FILES[:states]] do
    sh "cat #{COMPILED_FILES[:nationwide]} > #{COMPILED_FILES[:all]}"
    # FreeBSD tail is much slower than the sed variant, not so if on GNU...
    sh "sed '1d' #{COMPILED_FILES[:states]} >> #{COMPILED_FILES[:all]}"

end


desc "Compile nationwide CSV file, for years #{START_YEAR} through #{END_YEAR}"
file COMPILED_FILES[:nationwide] => FETCHED_NATIONFILES do
    cmd = shelljoin(['python',
        SCRIPTS_DIR.join('compile.py'),
        'nationwide',
        DIRS[:fetched_nationwide]])
    shell.system(cmd) > COMPILED_FILES[:nationwide].to_s
end


desc 'Compile states CSV file'
file COMPILED_FILES[:states] => FETCHED_STATEFILES do
    cmd = shelljoin(['python',
        SCRIPTS_DIR.join('compile.py'),
        'states',
        DIRS[:fetched_states]])
    shell.system(cmd) > COMPILED_FILES[:states].to_s
end

task :test do
    puts shell.system('curl http://www.example.com')
end


